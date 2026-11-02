#!/usr/bin/env python3
"""Order Ticket & Paper Trading Broker for day-trader-india.
Generates order tickets for Indian discount brokers (Zerodha MIS, Dhan Intraday,
Angel One) and maintains a free local paper trading ledger.
Paper trading by default. Never sends an order without explicit confirmation.

Commands:
    python3 ticket.py preview      # Show order ticket from trader/order.json
    python3 ticket.py paper        # Execute paper trade -> trader/trades.json
    python3 ticket.py pnl          # View active positions and paper trading ledger
"""

import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))


def get_trader_dir():
    if "TRADER_DIR" in os.environ:
        return os.environ["TRADER_DIR"]
    if os.path.exists("trader"):
        return "trader"
    elif os.path.exists("../trader"):
        return "../trader"
    return "trader"


def cmd_preview():
    trader_dir = get_trader_dir()
    order_path = os.path.join(trader_dir, "order.json")
    if not os.path.exists(order_path):
        print("No order.json found. Run trader-budget first.")
        return

    with open(order_path, "r", encoding="utf-8") as f:
        order = json.load(f)

    print(f"\n{'='*56}\n  INDIAN BROKER ORDER TICKET (MIS / INTRADAY)\n{'='*56}")
    print(f"  Exchange           : NSE")
    print(f"  Symbol             : {order['symbol']}")
    print(f"  Action             : {'BUY' if order['direction'] == 'LONG' else 'SELL'}")
    print(f"  Order Type         : LIMIT (Bracket / Cover Order)")
    print(f"  Product Code       : MIS (Intraday with 5x leverage)")
    print(f"  Quantity           : {order['quantity']} shares")
    print(f"  Entry Limit Price  : ₹{order['entry_price']}")
    print(f"  Stop-Loss Trigger  : ₹{order['stop_loss']}")
    print(f"  Target Price       : ₹{order['target']}")
    print(f"  Total Margin Block : ₹{order['margin_required_inr']:,}")
    print(f"  Max Rupee Risk     : ₹{order['max_risk_inr']:,}")
    print(f"{'='*56}")
    print("Mode: PAPER TRADING (Safe simulation). Run 'python3 ticket.py paper' to fill.\n")


def cmd_paper():
    trader_dir = get_trader_dir()
    order_path = os.path.join(trader_dir, "order.json")
    if not os.path.exists(order_path):
        print("No order.json found. Run trader-budget first.")
        return

    with open(order_path, "r", encoding="utf-8") as f:
        order = json.load(f)

    now_ist = datetime.now(timezone.utc).astimezone(IST)
    trade_entry = {
        "id": f"TRD-{int(time.time())}",
        "timestamp": now_ist.strftime("%Y-%m-%d %H:%M:%S IST"),
        "symbol": order["symbol"],
        "direction": order["direction"],
        "quantity": order["quantity"],
        "entry_price": order["entry_price"],
        "stop_loss": order["stop_loss"],
        "target": order["target"],
        "margin_blocked": order["margin_required_inr"],
        "status": "OPEN",
        "current_pnl_inr": 0.0
    }

    trades_file = os.path.join(trader_dir, "trades.json")
    trades = []
    if os.path.exists(trades_file):
        with open(trades_file, "r", encoding="utf-8") as f:
            trades = json.load(f)

    trades.append(trade_entry)
    with open(trades_file, "w", encoding="utf-8") as f:
        json.dump(trades, f, indent=2)

    print(f"  🎉 [Paper Execution Filled]")
    print(f"  Position ID : {trade_entry['id']}")
    print(f"  Bought {order['quantity']} {order['symbol']} @ ₹{order['entry_price']}")
    print(f"  Stop: ₹{order['stop_loss']} | Target: ₹{order['target']}")
    print(f"  Logged to {trades_file}\n")


def cmd_pnl():
    trader_dir = get_trader_dir()
    trades_file = os.path.join(trader_dir, "trades.json")
    if not os.path.exists(trades_file):
        print("No paper trades executed yet.")
        return

    with open(trades_file, "r", encoding="utf-8") as f:
        trades = json.load(f)

    print(f"\n{'='*64}\n  PAPER TRADING PORTFOLIO & INTRADAY LEDGER\n{'='*64}")
    total_realized = 0.0
    for t in trades:
        print(f"  [{t['id']}] {t['symbol']:12} {t['direction']:5} | {t['quantity']:4d} shares @ ₹{t['entry_price']}")
        print(f"    SL: ₹{t['stop_loss']} | TGT: ₹{t['target']} | Status: {t['status']}")
    print(f"{'='*64}\n")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return

    cmd = sys.argv[1].lower()
    if cmd == "preview":
        cmd_preview()
    elif cmd == "paper":
        cmd_paper()
    elif cmd == "pnl":
        cmd_pnl()
    else:
        print(f"Unknown command: {cmd}\n{__doc__}")


if __name__ == "__main__":
    main()
