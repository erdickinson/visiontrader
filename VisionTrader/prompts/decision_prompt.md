Given the previous ChartState and TradePlan (if any), and the new screenshot, decide one of: WAIT, ARM, ENTER, ADJUST, EXIT, CANCEL.
Return STRICT JSON ActionDecision only.
- ENTER only when all required fields are present and the plan is valid.
- EXIT if stop/target appears hit or the plan is invalidated.
- ADJUST if the plan should be modified due to new structure (tighten stop, partial TP, etc.).
- CANCEL to abandon a stale/invalid plan.
