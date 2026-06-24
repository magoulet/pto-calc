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


class AppConfig(BaseModel):
    employment_start_date: str
    schedule_file: str
    standard_pto: StandardPTOConfig
    flexible_pto: FlexiblePTOConfig
