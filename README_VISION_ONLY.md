# Vision-Only Addon (GUI Executor + Price-Scale Calibration)

This addon lets you run the **Vision Trader MVP** without a broker API by using
**hotkeys** and **mouse automation** on your charting/trading platform.

> ⚠️ **High risk**: GUI automation can misfire due to focus, DPI scaling, or UI updates.
> Start with **dry-run**. Then **paper** only. Live use at your own risk.

## What this adds

- A drop-in replacement `executor.py` that implements a **vision-only GUI actuator**.
- `calibrate_price_scale.py` that OCRs the price scale to learn a linear pixel↔price mapping each session.
- A sample `gui_config.yaml` with hotkey mappings and ROIs for the chart and price scale.

## How it works

1. **Calibrate** the price scale once after you position/zoom your chart:
   ~~~bash
   python calibrate_price_scale.py --config config.yaml
   ~~~
   This saves `logs/gui_mapping.json` with a linear mapping `price = m*y + b` for your current view.

2. **Run the main loop**. When the LLM returns an `ActionDecision` with an `OrderSpec`:
   - `market` orders: executor triggers the configured hotkey (no cursor math).
   - `limit/stop` orders with `price`: executor converts `price → y-pixel` using the mapping,
     moves the mouse to `(x_right_margin, y)`, and presses your **“place order at cursor”** hotkey.

3. **Adjust/Exit**:
   - `EXIT`: sends the configured `exit_all` hotkey.
   - `ADJUST` (optional): if an updated stop/target price is provided and a hotkey like
     “Move stop to cursor” exists, the executor will move to the y for that price and fire it.

> ✅ Most platforms (NinjaTrader, Sierra, Quantower, etc.) allow hotkeys like “Place Buy Limit at cursor” and “Exit all”. Configure these once and let the executor trigger them.  
> ❌ If your platform has no relevant hotkeys, pure clicking through menus is **much less reliable**.

## Setup

1. Drop these files into the root of your existing `vision_trader_mvp/` project, **overwriting `executor.py`**.
2. Edit your main `config.yaml` and add a `gui:` section like the sample in `gui_config.yaml`.
3. Ensure **Tesseract** is installed on your system so `pytesseract` can OCR the scale:
   - Windows: install from https://github.com/UB-Mannheim/tesseract/wiki and note the install path.
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`
   - If needed, set `tesseract_cmd` in `gui.tesseract_cmd` in your config.

## Sample `gui` config (copy into your `config.yaml`)

```yaml
gui:
  # Screen regions inside your screenshot_region (pixels, relative to top-left of monitor)
  chart_roi: { x: 120, y: 140, width: 1450, height: 820 }   # where bars are
  scale_roi: { x: 1580, y: 140, width:  60, height: 820 }   # price axis area

  # Hotkeys (edit to match your platform)
  hotkeys:
    buy_limit_at_cursor:   ["ctrl","alt","b"]
    sell_limit_at_cursor:  ["ctrl","alt","s"]
    buy_market:            ["ctrl","alt","m"]
    sell_market:           ["ctrl","alt","n"]
    exit_all:              ["ctrl","alt","x"]
    move_stop_to_cursor:   ["ctrl","alt","1"]   # optional
    move_target_to_cursor: ["ctrl","alt","2"]   # optional

  # Cursor placement
  right_margin_px: 20      # click near the right edge of chart area
  move_duration_ms: 80
  post_hotkey_sleep_ms: 120

  # Tesseract (optional explicit path)
  tesseract_cmd: null
