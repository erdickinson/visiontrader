# Vision Trader MVP (screenshot-driven orchestration)

> **Important**: Educational starter kit for building a *vision-assisted* trading orchestration loop. Not financial advice. Use only in **dry-run**/**paper** modes until you are confident and compliant with your broker and local regulations.

This repo shows how to:
1) Capture chart screenshots at a steady cadence.
2) Send the image to an LLM (or use a mock) to extract *state*, propose a *trade plan*, and return an *action decision*.
3) Enforce guardrails (max risk, freshness, trading hours, daily loss limit).
4) Place actions either by **GUI automation** (clicks/keystrokes) or **broker API** (preferred), via a single `Executor` interface.
5) Log everything to disk to make post-trade review and offline backtesting possible.

The system is designed to be **model-agnostic** and **platform-agnostic**. You can plug in OpenAI, local VLMs, or other providers; and you can drive IBKR, Alpaca, Tradovate, Quantower (via bridge), or a GUI clicker.

---

## Quick start

1. **Install** (Python 3.10+ recommended):
   ~~~bash
   pip install -r requirements.txt
   ~~~

2. **Configure** `config.yaml` (region, cadence, risk). At minimum, set `screenshot_region` to the monitor area of your chart (x, y, width, height in pixels).

3. **Run in dry-run** (no orders; prints decisions and logs them):
   ~~~bash
   python main.py --mode dry-run
   ~~~

4. **Paper mode** with GUI click stubs (still *no live orders*):
   ~~~bash
   python main.py --mode paper --actuator gui
   ~~~

5. **Paper mode** with a broker stub (replace with your connector):
   ~~~bash
   python main.py --mode paper --actuator broker
   ~~~

By default, the code uses a **Mock LLM** so you can see the loop run immediately. Swap to a real model by editing `vision_llm.py` and following the `LLMClient` template.

---

## Why screenshots (and what to standardize)

If you insist on vision-first control, make your chart **LLM-friendly**:
- Fixed background, hide grid, consistent zoom.
- Keep only essential overlays (e.g., VWAP, 20/50 EMA) with consistent colors.
- Ensure instrument & timeframe labels are visible and large enough for OCR.
- Place price scale and last price in predictable positions.
- Avoid pop-ups/alerts covering the chart.

**But**: direct market data + broker APIs are more reliable. Screenshots are brittle. This repo keeps screenshots for perception, but you can add a data feed and use screenshots only as a cross-check.

---

## States & flow

