from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.configs.doctor_availability import DoctorAvailability

router = APIRouter(tags=["Doctor Availability"])

doctor_availability = DoctorAvailability()


@router.get(
    "/report",
    status_code=status.HTTP_200_OK,
    summary="Get Doctor Availability Report",
    description="Retrieve a detailed report of current doctor availability."
)
async def get_availability_report():
    try:
        return doctor_availability.get_availability_report()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Failed to generate availability report", "details": str(e)}
        )


@router.get(
    "/next-slot",
    status_code=status.HTTP_200_OK,
    summary="Find Next Available Slot",
    description="Retrieve the next available appointment slot based on dementia level."
)
async def find_next_slot(dementia_level: str = "NORMAL"):
    try:
        return doctor_availability.find_next_available_slot(dementia_level)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Failed to find next available slot", "details": str(e)}
        )
