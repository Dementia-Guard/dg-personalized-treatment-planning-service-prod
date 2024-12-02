from pydantic import BaseModel, Field, ConfigDict, validator, field_validator
from typing import Optional


class PatientInput(BaseModel):
    id: Optional[str] = Field(None, description="Optional patient ID")
    firstName: str = Field(..., min_length=2, max_length=50, description="Patient's first name")
    lastName: str = Field(..., min_length=2, max_length=50, description="Patient's last name")
    age: Optional[int] = Field(None, gt=0, le=120, description="Patient's age")
    cdrScore: float = Field(
        ...,
        ge=0,
        le=3,
        description="Clinical Dementia Rating score (0-3)"
    )
    mmseScore: float = Field(
        ...,
        gt=0,
        le=30,
        description="Mini-Mental State Examination score (0-30)"
    )
    additionalNotes: Optional[str] = Field(None, max_length=500, description="Additional patient notes")
    fullName: str
    caregiverAvailability: str

    @field_validator("firstName", "lastName")
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()
