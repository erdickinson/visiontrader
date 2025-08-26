from __future__ import annotations
import json, base64, time
from typing import Optional, Tuple
from loguru import logger
from schemas import ChartState, TradePlan, ActionDecision, AdjustmentRule, OrderSpec, ScreenshotMeta

class VisionTraderLLM:
    """LLM facade. Uses a mock by default; swap in a real client following the _call_model() template."""
    def __init__(self, provider: str = "mock"):
        self.provider = provider

    def analyze(self, image_path: str, meta: ScreenshotMeta) -> Tuple[ChartState, TradePlan, ActionDecision]:
        if self.provider == "mock":
            return self._mock_outputs(image_path, meta)
        else:
            # Implement _call_model(image_bytes) and parse JSON according to prompts
            return self._call_model(image_path, meta)

    def _mock_outputs(self, image_path: str, meta: ScreenshotMeta):
        # Simple deterministic mock: alternate WAIT/ARM based on image hash parity
        parity = int(meta.hash[-1], 16) % 2
        chart = ChartState(
            instrument=meta.instrument_hint or "US500",
            timeframe=meta.timeframe_hint or "M5",
            trend_bias="long" if parity == 0 else "short",
            last_price=None,
            volatility=None,
            key_levels=[],
            notes="mocked state",
            confidence=0.6,
        )
        plan = TradePlan(
            instrument=chart.instrument,
            setup_name="MockPullback",
            bias="long" if parity == 0 else "short",
            entry_type="limit",
            entry_price=None,
            stop_price=None,
            target_price=None,
            notes="mocked plan",
            confidence=0.55,
        )
        action = ActionDecision(
            action="ARM" if parity == 0 else "WAIT",
            reason="mock decision based on hash parity",
            order=None
        )
        return chart, plan, action

    def _call_model(self, image_path: str, meta: ScreenshotMeta):
        # Template for a real provider
        # 1) read image
        with open(image_path, "rb") as f:
            b = f.read()
        b64 = base64.b64encode(b).decode("utf-8")

        # 2) Construct prompt (system + user) that asks for STRICT JSON for ChartState, TradePlan, ActionDecision.
        #    See prompts in ./prompts. Your provider must support image inputs.
        # 3) Call the provider and parse JSON safely with json.loads.
        # 4) Validate with Pydantic models.
        raise NotImplementedError("Plug in your LLM provider here per your API. See prompts/ for guidance.")
