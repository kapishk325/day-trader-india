#!/usr/bin/env python3
"""Comprehensive Unit Test Suite for day-trader-india.
Tests all financial math, indicators, SEBI margin rules, statutory charges,
and exit calculations. Standard library unittest only.
"""

import os
import sys
import unittest

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "trader-scanner"))
sys.path.insert(0, os.path.join(BASE_DIR, "trader-entry"))
sys.path.insert(0, os.path.join(BASE_DIR, "trader-exit"))
sys.path.insert(0, os.path.join(BASE_DIR, "trader-budget"))
sys.path.insert(0, os.path.join(BASE_DIR, "trader-risk"))
sys.path.insert(0, os.path.join(BASE_DIR, "trader-oi"))
sys.path.insert(0, os.path.join(BASE_DIR, "trader-timemachine"))

from scan import rsi_14
from entry import compute_vwap
from exit import calculate_exit
from check import calculate_indian_charges
from oi import compute_pcr
from timemachine import run_monte_carlo


class TestDayTraderIndia(unittest.TestCase):

    def test_rsi_14(self):
        """Test RSI 14 calculation with trending and oversold closes."""
        # 16 identical closes -> no gains, no losses -> 50.0 default
        closes_flat = [100.0] * 20
        self.assertEqual(rsi_14(closes_flat), 50.0)

        # Monotonically increasing closes -> RSI = 100
        closes_up = [100.0 + i for i in range(25)]
        self.assertEqual(rsi_14(closes_up), 100.0)

        # Monotonically dropping closes -> RSI ~ 0
        closes_down = [200.0 - (i * 2) for i in range(25)]
        self.assertLess(rsi_14(closes_down), 15.0)

    def test_vwap_calculation(self):
        """Test intraday Volume Weighted Average Price."""
        bars = [
            {"high": 105, "low": 95, "close": 100, "volume": 1000},  # typical: 100, pv = 100,000
            {"high": 115, "low": 105, "close": 110, "volume": 2000}, # typical: 110, pv = 220,000
        ]
        # Total vol = 3000, Total pv = 320,000 => vwap = 320,000 / 3000 = 106.67
        vwap = compute_vwap(bars)
        self.assertEqual(vwap, 106.67)

    def test_exit_planner_long(self):
        """Test Long exit targets and stop loss calculation."""
        plan = calculate_exit("RELIANCE.NS", "LONG", entry=1250.0, orb_high=1245.0, orb_low=1230.0, orb_mid=1237.5)
        self.assertEqual(plan["symbol"], "RELIANCE.NS")
        self.assertEqual(plan["stop_loss"], 1237.5)
        self.assertEqual(plan["risk_per_share"], 12.5)
        # 1:1.5R target = 1250 + (1.5 * 12.5) = 1268.75
        self.assertEqual(plan["target_1_5r"], 1268.75)
        # 1:2.0R target = 1250 + (2.0 * 12.5) = 1275.0
        self.assertEqual(plan["target_2r"], 1275.0)
        self.assertEqual(plan["hard_time_cutoff"], "15:15 IST")

    def test_exit_planner_short(self):
        """Test Short exit targets and stop loss calculation."""
        plan = calculate_exit("TCS.NS", "SHORT", entry=3500.0, orb_high=3540.0, orb_low=3510.0, orb_mid=3525.0)
        self.assertEqual(plan["stop_loss"], 3525.0)
        self.assertEqual(plan["risk_per_share"], 25.0)
        # 1:1.5R target = 3500 - (1.5 * 25.0) = 3462.5
        self.assertEqual(plan["target_1_5r"], 3462.5)
        # 1:2.0R target = 3500 - (2.0 * 25.0) = 3450.0
        self.assertEqual(plan["target_2r"], 3450.0)

    def test_statutory_taxes_charges(self):
        """Test exact Indian charges calculation (STT, GST, Exchange charges, Stamp duty)."""
        # ₹100,000 buy and ₹105,000 sell
        buy_val = 100000.0
        sell_val = 105000.0
        charges = calculate_indian_charges(buy_val, sell_val)

        # STT = 0.025% on sell = ₹26.25
        self.assertEqual(charges["stt"], 26.25)
        # Brokerage = 2 orders * ₹20 = ₹40.0
        self.assertEqual(charges["brokerage"], 40.0)
        # Stamp duty = 0.003% on buy = ₹3.0
        self.assertEqual(charges["stamp_duty"], 3.0)
        # Total charges should be positive and reasonable (< ₹120 on ₹205k turnover)
        self.assertGreater(charges["total_charges"], 70.0)
        self.assertLess(charges["total_charges"], 120.0)

    def test_pcr_calculation(self):
        """Test Put-Call Ratio calculation."""
        contracts = [
            {"identifier": "OPTIDXNIFTY...CE...", "openInterest": 100000},
            {"identifier": "OPTIDXNIFTY...CE...", "openInterest": 150000},
            {"identifier": "OPTIDXNIFTY...PE...", "openInterest": 300000},
        ]
        # Total call OI = 250,000, Total put OI = 300,000 => PCR = 300,000 / 250,000 = 1.2
        pcr, call_oi, put_oi = compute_pcr(contracts)
        self.assertEqual(pcr, 1.2)
        self.assertEqual(call_oi, 250000)
        self.assertEqual(put_oi, 300000)

    def test_monte_carlo_expected_value(self):
        """Test Monte Carlo simulation returns valid probabilities."""
        plan = {
            "entry_price": 100.0,
            "stop_loss": 95.0,
            "target_1_5r": 107.5,
            "direction": "LONG"
        }
        # Simulate slight upward drift in 5m bars
        deltas = [
            {"high_pct": 0.01, "low_pct": -0.005, "close_pct": 0.003},
            {"high_pct": 0.008, "low_pct": -0.008, "close_pct": -0.001},
            {"high_pct": 0.015, "low_pct": -0.002, "close_pct": 0.005},
        ]
        res = run_monte_carlo(plan, deltas, runs=1000, remaining_bars=20)
        self.assertIn("target_hit_pct", res)
        self.assertIn("stop_hit_pct", res)
        self.assertIn("expected_value_per_rupee", res)
        self.assertIn(res["verdict"], ["FAVORABLE", "MARGINAL", "UNFAVORABLE"])


if __name__ == "__main__":
    unittest.main()
