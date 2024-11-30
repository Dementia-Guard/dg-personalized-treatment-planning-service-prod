from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from datetime import datetime


class DementiaLevel(str, Enum):
    NORMAL = "NORMAL"
    MILD = "MILD"
    MODERATE = "MODERATE"
    SEVERE = "SEVERE"


class TreatmentPlanOutput(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    dementia_level: DementiaLevel
    visit_frequency: Optional[int]
    treatment_recommendation: Optional[str]
    next_appointment: Optional[str]
    error: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
