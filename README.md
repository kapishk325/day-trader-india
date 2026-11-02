# Day Trader India (day-trader-india)

12 Claude & Antigravity skills for day trading the **Indian Stock Market (NSE / BSE)**: scan liquid F&O charts, track live FII/DII institutional flows, analyze Nifty Put-Call Ratio (PCR) and India VIX, time your entry bar-by-bar, plan exact stops with a mandatory 15:15 IST auto-squareoff hard stop, and replay every outcome 10,000 times before risking a single rupee.

**100% Free, MIT, No Signup, Zero API Keys.** Standard Python 3 standard library only. The tools read free public data from Yahoo Finance Indian endpoints (`.NS` tickers, `^NSEI`, `^INDIAVIX`), official NSE Archives (Nifty 100/500 universe), and official NSE live institutional feeds (FII/DII cash activity, Bulk & Block deals, and Option Chains).

Nothing in this pack can place a live order on its own. **Paper trading is the default.**

---

## The Twelve Skills

| Command / Skill | Role | What It Does (Indian Market Specifics) |
| :--- | :--- | :--- |
| **`/trader-scanner`** | **NSE Chart Scanner** | Scans the liquid **NSE Nifty 100 / F&O universe** for 15-minute Opening Range Breakouts (ORBs), 20-day highs, bull flags, and oversold bounces. |
| **`/trader-fii-dii`** | **Institutional Flow Tracker** | *(Replaces US Congress tracker)* Reads official **NSE daily FII & DII net cash buy/sell figures** and **Bulk & Block deals** to detect big money accumulation. |
| **`/trader-oi`** | **Open Interest & VIX** | Tracks live **Nifty & Bank Nifty Put-Call Ratio (PCR)**, Option Chain shifts, and **India VIX** volatility regimes. |
| **`/trader-news`** | **Market News Monitor** | Tracks breaking headlines and corporate catalysts from Moneycontrol, Economic Times, Livemint, and NSE releases. |
| **`/trader-entry`** | **Intraday Entry Timer** | Watches candidate charts bar by bar (5m) after the 09:15–09:30 IST opening range and confirms entry when price and VWAP align. |
| **`/trader-exit`** | **Exit & Auto-Squareoff Planner** | Sets Stop-Loss and Take-Profit (1:1.5R and 1:2R) before entry. Enforces a **mandatory 15:15 IST hard exit** to avoid broker auto-squareoff penalty charges (₹50+GST). |
| **`/trader-timemachine`** | **Monte Carlo Time Machine** | Replays the rest of the Indian trading session **10,000 times** from historical 5-minute candle distributions to report honest win/loss probabilities. |
| **`/trader-budget`** | **Position Sizer (INR)** | Sizes position in Indian Rupees (₹) to your exact risk tolerance under **SEBI's 5x MIS intraday margin leverage**. |
| **`/trader-risk`** | **SEBI Compliance & Tax Guard** | Calculates exact statutory Indian taxes (**STT, Exchange Turnover charges, GST, Stamp Duty, Brokerage**) and blocks trades with poor risk-reward or entries after 14:30 IST. |
| **`/trader-broker`** | **Order Ticket & Paper Simulator**| Generates broker-ready MIS bracket order tickets and maintains a local paper trading portfolio in `trader/trades.json`. |
| **`/trader-alerts`** | **Price & Time Milestone Alerts** | Rings on Target hit, Stop loss, and critical session times (**09:15 Open, 09:30 ORB set, 15:10 Pre-squareoff warning**). |
| **`/trader-analyst`** | **NSE Stock & Liquidity Facts** | Summarizes 52-week price extremes, 20-day average daily volumes, and valuation multiples. |

---

## How It Works: The Full Trade Loop

Everything stores state cleanly in a `trader/` directory in your workspace:

```
scanner -> fii-dii -> oi -> news -> entry -> exit -> timemachine -> budget -> risk -> broker
alerts: target, stop, 15:10 IST squareoff reminder
```

### Walkthrough Example: Reliance Industries (RELIANCE.NS)

1. **`python3 trader-scanner/scan.py indices`** at 09:20 IST:
   * NIFTY 50 is up +1.12%, India VIX is at 15.55 (Normal Volatility / Optimal for ORB trend following).
2. **`python3 trader-fii-dii/fiidii.py summary`**:
   * FIIs were net buyers (+₹3,598 Cr), DIIs absorbed liquidity. Institutional sentiment: **STRONG_BULLISH**.
3. **`python3 trader-oi/oi.py summary`**:
   * Nifty PCR is 1.22 (Bullish Put writing floor).
4. **`python3 trader-scanner/scan.py orb`** at 09:35 IST:
   * Scans 15-minute range (09:15–09:30 IST). RELIANCE.NS range is ₹1214.60 to ₹1231.60. Candle closes at ₹1234.50. **BULLISH ORB triggered**.
5. **`python3 trader-exit/exit.py plan`**:
   * Stop set at range midpoint: ₹1223.10 (Risk = ₹11.40/share).
   * Target 1 (1:1.5R) = ₹1251.60. Target 2 (1:2.0R) = ₹1257.30.
   * Hard Time Stop: **15:15 IST**.
6. **`python3 trader-timemachine/timemachine.py replay`**:
   * Replays the remaining session 10,000 times from Reliance's historical 5m bars: Target hit 39.4%, Stop hit 40.2%, Flat by close 20.4%. Expected Value: **+₹0.19 per ₹1 risked** (Favorable edge).
7. **`python3 trader-budget/size.py size --risk 1500 --capital 100000`**:
   * Rupee budget ₹1,500 risk $\implies$ 131 shares (Value: ₹161,719). Under SEBI 5x MIS leverage, Margin required is ₹32,343 (32.3% of capital).
8. **`python3 trader-risk/check.py check`**:
   * Calculates ₹106.69 in total statutory charges (STT: ₹40.99, Brokerage: ₹40.00, GST+Exchange: ₹20.52, Stamp duty: ₹4.85). Net potential profit: ₹2,133.41.
9. **`python3 trader-broker/ticket.py paper`**:
   * Logs paper execution into `trader/trades.json`.
10. **`python3 trader-alerts/alerts.py check`**:
   * Monitors live tick. Target hit at ₹1263.60! Position flagged as complete.

---

## Installation

### For Claude Code
Clone the repository and copy the skills into your Claude skills directory:
```bash
git clone https://github.com/<your-username>/day-trader-india.git
cp -r day-trader-india/trader-* ~/.claude/skills/
```

### For Google Antigravity (`agy`)
Copy the skills directly into your `.agents/skills` directory:
```bash
git clone https://github.com/<your-username>/day-trader-india.git
cp -r day-trader-india/trader-* ~/.agents/skills/
```

### Standalone CLI / Chat
No agent harness? You can run any tool directly from your terminal:
```bash
cd day-trader-india
python3 trader-scanner/scan.py indices
python3 trader-fii-dii/fiidii.py flows
python3 trader-oi/oi.py vix
```

---

## Prerequisites
* Python 3.8 or newer.
* `curl` (pre-installed on Linux and macOS).
* **Zero external Python libraries to install** (No `pip install` required!).

---

## Disclaimer
*This project is for educational, analytical, and research purposes only. Day trading equities and derivatives carries substantial risk of financial loss. According to SEBI studies, over 90% of individual intraday and F&O traders incur net losses. Paper trade and practice disciplined risk management before allocating real capital.*

## License
MIT License. Free and open source.
