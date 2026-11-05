from typing import List, Optional

from pydantic import BaseModel, Field


class StandardPTOConfig(BaseModel):
    start_balance: float = 0
    max_rollover: float
    cap: Optional[float] = None
    yearly_accrual: List[float]


class FlexiblePTOConfig(BaseModel):
    start_balance: float = 0
    max_rollover: float
    cap: Optional[float] = None
    annual_grant: float
    monthly_accrual: float


class DisplayConfig(BaseModel):
    # Rolling window (months around today) for display purposes only.
    lookback_months: int = Field(default=6, ge=0)
    lookforward_months: int = Field(default=12, ge=0)


class AppConfig(BaseModel):
    employment_start_date: str
    schedule_file: str
    standard_pto: StandardPTOConfig
    flexible_pto: FlexiblePTOConfig
    display: DisplayConfig = DisplayConfig()
