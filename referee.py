from __future__ import annotations
from typing import Tuple
from datetime import datetime, timezone
from schemas import ChartState, TradePlan, ActionDecision, RefereeVerdict
from loguru import logger

def within_age(meta_ts, now, max_ms) -> bool:
    delta = (now - meta_ts).total_seconds() * 1000.0
    return delta <= max_ms

def enforce(risk_cfg: dict, max_image_age_ms: int, meta_ts, decision: ActionDecision, plan: TradePlan) -> Tuple[RefereeVerdict, ActionDecision]:
    now = datetime.now(timezone.utc)
    if not within_age(meta_ts.replace(tzinfo=timezone.utc), now, max_image_age_ms):
        reason = f"Image too old; age exceeds {max_image_age_ms} ms"
        logger.warning(reason)
        return RefereeVerdict(ok=False, downgraded=True, new_action="WAIT", reason=reason), ActionDecision(action="WAIT", reason=reason)

    # Risk checks (very simplified for MVP)
    if plan.risk_usd and plan.risk_usd > float(risk_cfg.get("max_risk_per_trade_usd", 0)):
        reason = f"Risk per trade {plan.risk_usd} exceeds limit"
        logger.warning(reason)
        return RefereeVerdict(ok=False, downgraded=True, new_action="WAIT", reason=reason), ActionDecision(action="WAIT", reason=reason)

    # Placeholder daily loss logic: assume external PnL tracker populates this.
    # For MVP, pass-through if action is not ENTER.
    if decision.action == "ENTER":
        # You can add additional checks here before permitting ENTRY
        pass

    return RefereeVerdict(ok=True), decision
