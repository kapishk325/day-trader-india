#!/usr/bin/env python3
"""Generates visual assets for day-trader-india (Social Banner & Demo Animation)."""

import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = "/home/kapish/day-trader-india/assets"
os.makedirs(ASSETS_DIR, exist_ok=True)


def create_banner():
    width, height = 1280, 640
    img = Image.new("RGB", (width, height), color="#0D1117")
    draw = ImageDraw.Draw(img)

    # Gradient top accent bar (Indian flag colors: Saffron, White, Green)
    draw.rectangle([0, 0, width // 3, 6], fill="#FF9933")
    draw.rectangle([width // 3, 0, (2 * width) // 3, 6], fill="#FFFFFF")
    draw.rectangle([(2 * width) // 3, 0, width, 6], fill="#138808")

    # Background grid lines for fintech aesthetic
    for x in range(0, width, 40):
        draw.line([(x, 0), (x, height)], fill="#161B22", width=1)
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill="#161B22", width=1)

    # Title & Subtitle
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        font_mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 15)
        font_mono_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 16)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_mono = ImageFont.load_default()
        font_mono_bold = ImageFont.load_default()

    draw.text((60, 60), "Day Trader India", fill="#58A6FF", font=font_title)
    draw.text((60, 130), "12-Skill Autonomous AI Day Trading Suite for NSE & BSE", fill="#C9D1D9", font=font_sub)
    draw.text((60, 165), "100% Free • Zero Sign-In • No API Keys • SEBI 5x MIS Leverage Guard", fill="#8B949E", font=font_sub)

    # Terminal Window Box
    term_x, term_y, term_w, term_h = 60, 220, 1160, 360
    draw.rounded_rectangle([term_x, term_y, term_x + term_w, term_y + term_h], radius=10, fill="#010409", outline="#30363D", width=2)
    # Header bar
    draw.rounded_rectangle([term_x, term_y, term_x + term_w, term_y + 36], radius=10, fill="#161B22")
    draw.rectangle([term_x, term_y + 20, term_x + term_w, term_y + 36], fill="#161B22")
    # Window buttons
    draw.ellipse([term_x + 14, term_y + 12, term_x + 26, term_y + 24], fill="#FF5F56")
    draw.ellipse([term_x + 34, term_y + 12, term_x + 46, term_y + 24], fill="#FFBD2E")
    draw.ellipse([term_x + 54, term_y + 12, term_x + 66, term_y + 24], fill="#27C93F")
    draw.text((term_x + term_w // 2 - 80, term_y + 10), "bash - day-trader-india", fill="#8B949E", font=font_mono)

    # Terminal Content
    lines = [
        ("$ python3 trader-scanner/scan.py indices", "#79C0FF"),
        ("  NIFTY 50    :   23,440.80  (+387.70, +1.68%)  [🟢 STRONG BULLISH]", "#3FB950"),
        ("  BANK NIFTY  :   55,002.20  (+315.25, +0.58%)  [🟢 ACCUMULATION]", "#3FB950"),
        ("  INDIA VIX   :      15.50  (+0.20, +1.29%)    [🟡 NORMAL REGIME]", "#D29922"),
        ("", "#FFFFFF"),
        ("$ python3 trader-scanner/scan.py orb", "#79C0FF"),
        ("  🚀 BULLISH ORB : ASIANPAINT.NS  Breakout at ₹2,365.50 (15m Range: ₹2,363.90)", "#58A6FF"),
        ("  🚀 BULLISH ORB : BEL.NS         Breakout at ₹377.30   (15m Range: ₹376.80)", "#58A6FF"),
        ("  🔻 BEARISH ORB : BAJFINANCE.NS  Breakdown at ₹940.90  (15m Range: ₹941.60)", "#F85149"),
        ("", "#FFFFFF"),
        ("$ python3 trader-alerts/alerts.py check", "#79C0FF"),
        ("  ⚠️ TIME WARNING: Auto-squareoff hard stop at 15:15 IST (Enforced)", "#E3B341"),
        ("  🎯 TARGET REACHED for RELIANCE.NS at ₹1,300.00 (+5.31%)", "#3FB950"),
    ]

    curr_y = term_y + 50
    for text, color in lines:
        draw.text((term_x + 25, curr_y), text, fill=color, font=font_mono_bold)
        curr_y += 22

    banner_path = os.path.join(ASSETS_DIR, "social-preview.png")
    img.save(banner_path, "PNG")
    print(f"Created {banner_path}")


def create_demo_gif():
    width, height = 900, 480
    frames = []

    try:
        font_mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 14)
    except Exception:
        font_mono = ImageFont.load_default()
        font_bold = ImageFont.load_default()

    terminal_sequence = [
        # Frame 1: empty terminal
        [("$ day-trader-india (NSE/BSE Autonomous Day Trading Suite)", "#79C0FF")],
        # Frame 2: scan prompt
        [
            ("$ day-trader-india (NSE/BSE Autonomous Day Trading Suite)", "#79C0FF"),
            ("$ python3 trader-scanner/scan.py indices", "#58A6FF")
        ],
        # Frame 3: indices loaded
        [
            ("$ day-trader-india (NSE/BSE Autonomous Day Trading Suite)", "#79C0FF"),
            ("$ python3 trader-scanner/scan.py indices", "#58A6FF"),
            ("  NIFTY 50    :  23,440.80  (+387.70, +1.68%) 🟢", "#3FB950"),
            ("  BANK NIFTY  :  55,002.20  (+315.25, +0.58%) 🟢", "#3FB950"),
            ("  INDIA VIX   :     15.50  (+0.20, +1.29%)   🟡", "#D29922"),
        ],
        # Frame 4: orb scan
        [
            ("$ day-trader-india (NSE/BSE Autonomous Day Trading Suite)", "#79C0FF"),
            ("$ python3 trader-scanner/scan.py indices", "#58A6FF"),
            ("  NIFTY 50    :  23,440.80  (+387.70, +1.68%) 🟢", "#3FB950"),
            ("  INDIA VIX   :     15.50  (+0.20, +1.29%)   🟡", "#D29922"),
            ("$ python3 trader-scanner/scan.py orb", "#58A6FF"),
            ("  Scanning 100 liquid stocks for 15-min Opening Range Breakouts...", "#8B949E"),
            ("  🚀 BULLISH ORB: ASIANPAINT.NS  Breakout @ ₹2,365.50", "#79C0FF"),
            ("  🚀 BULLISH ORB: BEL.NS         Breakout @ ₹377.30", "#79C0FF"),
            ("  🔻 BEARISH ORB: BAJFINANCE.NS  Breakdown @ ₹940.90", "#F85149"),
        ],
        # Frame 5: risk & charges audit
        [
            ("$ python3 trader-risk/check.py charges --val 50000", "#58A6FF"),
            ("  Turnover: ₹100,000 | Brokerage: ₹40.00 | STT: ₹12.50", "#C9D1D9"),
            ("  GST: ₹7.84 | Stamp Duty: ₹1.50 | Exchange: ₹3.45", "#C9D1D9"),
            ("  TOTAL CHARGES: ₹65.39  (0.065% breakeven spread)", "#3FB950"),
            ("$ python3 trader-broker/ticket.py pnl", "#58A6FF"),
            ("  [TRD-1793] RELIANCE.NS  LONG 175 shs @ ₹1234.50 -> CMP ₹1300.00", "#C9D1D9"),
            ("  Live P&L: +₹11,462.50 (+5.31%) [🟢 IN PROFIT]", "#3FB950"),
            ("  Hard Stop: Mandatory Auto-Squareoff at 15:15 IST", "#E3B341"),
        ]
    ]

    for step_lines in terminal_sequence:
        img = Image.new("RGB", (width, height), color="#010409")
        draw = ImageDraw.Draw(img)

        # Header
        draw.rectangle([0, 0, width, 32], fill="#161B22")
        draw.ellipse([14, 10, 24, 20], fill="#FF5F56")
        draw.ellipse([32, 10, 42, 20], fill="#FFBD2E")
        draw.ellipse([50, 10, 60, 20], fill="#27C93F")
        draw.text((width // 2 - 80, 8), "day-trader-india (demo)", fill="#8B949E", font=font_mono)

        curr_y = 48
        for text, color in step_lines:
            draw.text((20, curr_y), text, fill=color, font=font_bold)
            curr_y += 24

        frames.append(img)

    gif_path = os.path.join(ASSETS_DIR, "demo.gif")
    # Save animated GIF with 1.8s delay between frames
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=[1200, 1500, 1800, 2200, 3000],
        loop=0
    )
    print(f"Created {gif_path}")


if __name__ == "__main__":
    create_banner()
    create_demo_gif()
