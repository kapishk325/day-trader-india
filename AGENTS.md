# AGENTS.md — Day Trader India Instructions

This repository contains 12 specialized tools for day trading the Indian Stock Market (NSE/BSE).
All tools use the Python standard library only and query free public endpoints. Zero API keys required.

## Available Skills & Workflow Order

Follow this sequence for any trade:

1. **`trader-scanner`**:
   * Pre-market: `python3 trader-scanner/scan.py indices` to check Nifty and India VIX.
   * `python3 trader-scanner/scan.py daily` to generate `trader/watchlist.json`.
   * Intraday (after 09:30 IST): `python3 trader-scanner/scan.py orb` for 15-minute Opening Range Breakouts.
2. **`trader-fii-dii`**:
   * `python3 trader-fii-dii/fiidii.py summary` to verify Foreign & Domestic institutional bias.
3. **`trader-oi`**:
   * `python3 trader-oi/oi.py summary` to check Nifty Put-Call Ratio (PCR) and India VIX volatility regime.
4. **`trader-news`**:
   * `python3 trader-news/news.py symbol --symbol SYMBOL.NS` to verify no adverse corporate news.
5. **`trader-entry`**:
   * `python3 trader-entry/entry.py watch --symbol SYMBOL.NS` to confirm a 5m candle close above the opening range with VWAP alignment.
6. **`trader-exit`**:
   * `python3 trader-exit/exit.py plan` to calculate Stop-Loss, Target 1 (1.5R), Target 2 (2R), and the 15:15 IST hard cutoff.
7. **`trader-timemachine`**:
   * `python3 trader-timemachine/timemachine.py replay` to simulate 10,000 Monte Carlo session outcomes.
8. **`trader-budget`**:
   * `python3 trader-budget/size.py size --risk <INR> --capital <INR>` to size shares to your exact rupee risk limit under 5x MIS leverage.
9. **`trader-risk`**:
   * `python3 trader-risk/check.py check` to calculate exact STT, GST, Exchange charges, and block entries after 14:30 IST.
10. **`trader-broker`**:
    * `python3 trader-broker/ticket.py paper` to simulate paper order execution into `trader/trades.json`.
11. **`trader-alerts`**:
    * `python3 trader-alerts/alerts.py check` to monitor live price vs stop and target levels.
