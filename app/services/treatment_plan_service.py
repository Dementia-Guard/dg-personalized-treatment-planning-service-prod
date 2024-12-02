from app.configs.expert_system import DementiaExpertSystem
from app.models.patient import PatientInput
from app.models.treatment_plan import TreatmentPlanOutput


class TreatmentPlanService:
    def __init__(self):
        self.expert_system = DementiaExpertSystem()

    def create_treatment_plan(self, patient: PatientInput) -> TreatmentPlanOutput:
        patient_data = {
            "firstName": patient.firstName,
            "lastName": patient.lastName,
            "cdr_Score": patient.cdrScore,
            "mmse_Score": patient.mmseScore,
            "caregiverAvailability": patient.caregiverAvailability,
        }
        treatment_plan = self.expert_system.generate_treatment_plan(patient_data)
        if not treatment_plan:
            raise ValueError("Unable to generate treatment plan")
        return TreatmentPlanOutput(**treatment_plan)
