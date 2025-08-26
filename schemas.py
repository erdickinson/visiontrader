from __future__ import annotations
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
from datetime import datetime

class ScreenshotMeta(BaseModel):
    path: str
    timestamp: datetime
    hash: str
    width: int
    height: int
    instrument_hint: Optional[str] = None
    timeframe_hint: Optional[str] = None

class ChartState(BaseModel):
    instrument: str = Field(..., description="Symbol or instrument inferred from chart")
    timeframe: str = Field(..., description="Timeframe like M1, M5, M15, H1, etc.")
    trend_bias: Literal["long", "short", "range", "unclear"]
    last_price: Optional[float] = None
    volatility: Optional[float] = Field(None, description="ATR or rough volatility proxy")
    key_levels: List[float] = Field(default_factory=list, description="Support/resistance/POIs")
    notes: Optional[str] = None
    confidence: float = Field(0.0, ge=0.0, le=1.0)

class AdjustmentRule(BaseModel):
    condition: str = Field(..., description="Natural language or simple DSL condition")
    action: str = Field(..., description="What to do if condition is met (e.g., tighten stop to X)")

class TradePlan(BaseModel):
    instrument: str
    setup_name: str
    bias: Literal["long","short","neutral"]
    entry_type: Literal["limit","market","stop"]
    entry_price: Optional[float] = None
    stop_price: Optional[float] = None
    target_price: Optional[float] = None
    take_profits: Optional[List[float]] = None
    invalidation: Optional[str] = None
    risk_usd: Optional[float] = None
    notes: Optional[str] = None
    adjustments: List[AdjustmentRule] = Field(default_factory=list)
    confidence: float = Field(0.5, ge=0.0, le=1.0)
    valid_until: Optional[datetime] = None

class OrderSpec(BaseModel):
    side: Literal["buy","sell"]
    qty: float
    type: Literal["market","limit","stop"]
    price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    client_tag: Optional[str] = None

class ActionDecision(BaseModel):
    action: Literal["WAIT","ARM","ENTER","ADJUST","EXIT","CANCEL"]
    reason: str
    order: Optional[OrderSpec] = None
    updated_plan: Optional[TradePlan] = None

class RefereeVerdict(BaseModel):
    ok: bool
    downgraded: bool = False
    new_action: Optional[str] = None
    reason: Optional[str] = None
