from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.models.patient import PatientInput
from app.models.treatment_plan import TreatmentPlanOutput
from app.services.treatment_plan_service import TreatmentPlanService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter()

treatment_plan_service = TreatmentPlanService()


@router.post(
    "/plan",
    response_model=TreatmentPlanOutput,
    status_code=status.HTTP_200_OK,
    summary="Generate Dementia Treatment Plan",
    description="Generate a personalized treatment plan based on patient data."
)
async def create_treatment_plan(patient: PatientInput):

    if patient.cdrScore is None or patient.mmseScore is None:
        logger.info(f"Invalid data: cdrScore = {patient.cdrScore}, mmseScore = {patient.mmseScore}")
        raise HTTPException(status_code=400, detail="Missing critical data: cdrScore or mmseScore")
    try:
        treatment_plan = treatment_plan_service.create_treatment_plan(patient)
        return treatment_plan
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Unexpected error occurred", "details": str(e)}
        )
