from experta import *
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Dict, Any
import logging
from .doctor_availability import DoctorAvailability

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DementiaLevel(Enum):
    NON_DEMENTED = auto()
    VERY_MILD_DEMENTED = auto()
    MILD_DEMENTED = auto()
    MODERATE_DEMENTED = auto()
    SEVERE_DEMENTED = auto()


class PatientInfo(Fact):
    """Represents patient's medical information"""
    pass


class TreatmentPlan(Fact):
    dementia_level: DementiaLevel
    visit_frequency: int
    treatment_recommendation: tuple
    next_appointment: str

    def __init__(self, dementia_level: DementiaLevel, visit_frequency: int, treatment_recommendation: tuple, next_appointment: str):
        super().__init__()
        self.dementia_level = dementia_level
        self.visit_frequency = visit_frequency
        self.treatment_recommendation = treatment_recommendation
        self.next_appointment = next_appointment


class DementiaExpertSystem(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.doctor_availability = DoctorAvailability()

    # Non-Demented (Normal cognition)
    @Rule(PatientInfo(cdr_Score=P(lambda x: x == 0.0),
                      mmse_Score=P(lambda x: x >= 24.0),
                      caregiver_Availability="AVAILABLE"))
    def non_demented_available(self):
        next_appointment = self.doctor_availability.find_next_available_slot('NON_DEMENTED')
        self.declare(TreatmentPlan(
            dementia_level=DementiaLevel.NON_DEMENTED,
            visit_frequency=365,
            treatment_recommendation=(
                "1. Annual cognitive screenings.",
                "2. Maintain healthy diet and regular exercise.",
                "3. Monitor for any signs of cognitive decline."
            ),
            next_appointment=next_appointment['full_datetime']
        ))

    @Rule(PatientInfo(cdr_Score=P(lambda x: x == 0.0),
                      mmse_Score=P(lambda x: x >= 24.0),
                      caregiver_Availability="NONE"))
    def non_demented_no_caregiver(self):
        next_appointment = self.doctor_availability.find_next_available_slot('NON_DEMENTED')
        self.declare(TreatmentPlan(
            dementia_level=DementiaLevel.NON_DEMENTED,
            visit_frequency=365,
            treatment_recommendation=(
                "1. Annual cognitive screenings.",
                "2. Suggest patient join a social group for mental stimulation.",
                "3. Educate family about monitoring cognitive health."
            ),
            next_appointment=next_appointment['full_datetime']
        ))

    # Very Mild Demented
    @Rule(PatientInfo(cdr_Score=P(lambda x: 0.0 < x <= 0.5),
                      mmse_Score=P(lambda x: 22.0 <= x <= 23.0),
                      caregiver_Availability="AVAILABLE"))
    def very_mild_demented_available(self):
        next_appointment = self.doctor_availability.find_next_available_slot('VERY_MILD_DEMENTED')
        self.declare(TreatmentPlan(
            dementia_level=DementiaLevel.VERY_MILD_DEMENTED,
            visit_frequency=180,
            treatment_recommendation=(
                "1. Introduce cognitive exercises.",
                "2. Train caregivers for early dementia management.",
                "3. Maintain structured routines and regular follow-ups."
            ),
            next_appointment=next_appointment['full_datetime']
        ))

    @Rule(PatientInfo(cdr_Score=P(lambda x: 0.0 < x <= 0.5),
                      mmse_Score=P(lambda x: 22.0 <= x <= 23.0),
                      caregiver_Availability="NONE"))
    def very_mild_demented_no_caregiver(self):
        next_appointment = self.doctor_availability.find_next_available_slot('VERY_MILD_DEMENTED')
        self.declare(TreatmentPlan(
            dementia_level=DementiaLevel.VERY_MILD_DEMENTED,
            visit_frequency=180,
            treatment_recommendation=(
                "1. Encourage cognitive exercises and social interactions.",
                "2. Recommend community programs for caregiver support.",
                "3. Provide educational resources on dementia care."
            ),
            next_appointment=next_appointment['full_datetime']
        ))

    # Mild Demented
    @Rule(PatientInfo(cdr_Score=P(lambda x: 0.5 < x <= 1.0),
                      mmse_Score=P(lambda x: 19.0 <= x <= 21.0),
                      caregiver_Availability="AVAILABLE"))
    def mild_demented_available(self):
        next_appointment = self.doctor_availability.find_next_available_slot('MILD_DEMENTED')
        self.declare(TreatmentPlan(
            dementia_level=DementiaLevel.MILD_DEMENTED,
            visit_frequency=90,
            treatment_recommendation=(
                "1. Begin memory aids and structured routines.",
                "2. Regular follow-ups to monitor progression.",
                "3. Cognitive stimulation therapies and low-dose medications if needed."
            ),
            next_appointment=next_appointment['full_datetime']
        ))

    @Rule(PatientInfo(cdr_Score=P(lambda x: 0.5 < x <= 1.0),
                      mmse_Score=P(lambda x: 19.0 <= x <= 21.0),
                      caregiver_Availability="NONE"))
    def mild_demented_no_caregiver(self):
        next_appointment = self.doctor_availability.find_next_available_slot('MILD_DEMENTED')
        self.declare(TreatmentPlan(
            dementia_level=DementiaLevel.MILD_DEMENTED,
            visit_frequency=90,
            treatment_recommendation=(
                "1. Introduce cognitive rehabilitation and support groups.",
                "2. Consider a visiting caregiver or family member for assistance.",
                "3. Promote routine and structure in daily activities."
            ),
            next_appointment=next_appointment['full_datetime']
        ))

    # Moderate Demented
    @Rule(PatientInfo(cdr_Score=P(lambda x: 1.0 < x <= 2.0),
                      mmse_Score=P(lambda x: 10.0 <= x <= 18.0),
                      caregiver_Availability="AVAILABLE"))
    def moderate_demented_available(self):
        next_appointment = self.doctor_availability.find_next_available_slot('MODERATE_DEMENTED')
        self.declare(TreatmentPlan(
            dementia_level=DementiaLevel.MODERATE_DEMENTED,
            visit_frequency=60,
            treatment_recommendation=(
                "1. Introduce medication to slow cognitive decline.",
                "2. Educate caregivers on handling behavioral symptoms.",
                "3. Regular medical evaluations and introduce safety measures at home."
            ),
            next_appointment=next_appointment['full_datetime']
        ))

    @Rule(PatientInfo(cdr_Score=P(lambda x: 1.0 < x <= 2.0),
                      mmse_Score=P(lambda x: 10.0 <= x <= 18.0),
                      caregiver_Availability="NONE"))
    def moderate_demented_no_caregiver(self):
        next_appointment = self.doctor_availability.find_next_available_slot('MODERATE_DEMENTED')
        self.declare(TreatmentPlan(
            dementia_level=DementiaLevel.MODERATE_DEMENTED,
            visit_frequency=60,
            treatment_recommendation=(
                "1. Introduce medications for agitation and behavioral issues.",
                "2. Promote safety at home, and consider installing monitoring systems.",
                "3. Educate the family about dementia progression and caregiving."
            ),
            next_appointment=next_appointment['full_datetime']
        ))

    # Severe Demented
    @Rule(PatientInfo(cdr_Score=P(lambda x: x > 2.0),
                      mmse_Score=P(lambda x: x < 10.0),
                      caregiver_Availability="AVAILABLE"))
    def severe_demented_available(self):
        next_appointment = self.doctor_availability.find_next_available_slot('SEVERE_DEMENTED')
        self.declare(TreatmentPlan(
            dementia_level=DementiaLevel.SEVERE_DEMENTED,
            visit_frequency=30,
            treatment_recommendation=(
                "1. Implement comprehensive end-of-life care.",
                "2. Consider full-time care facilities.",
                "3. Address medical complications and improve quality of life."
            ),
            next_appointment=next_appointment['full_datetime']
        ))

    @Rule(PatientInfo(cdr_Score=P(lambda x: x > 2.0),
                      mmse_Score=P(lambda x: x < 10.0),
                      caregiver_Availability="NONE"))
    def severe_demented_no_caregiver(self):
        next_appointment = self.doctor_availability.find_next_available_slot('SEVERE_DEMENTED')
        self.declare(TreatmentPlan(
            dementia_level=DementiaLevel.SEVERE_DEMENTED,
            visit_frequency=30,
            treatment_recommendation=(
                "1. Move to a full-time care facility.",
                "2. Assign a multidisciplinary care team.",
                "3. Implement a comprehensive end-of-life care plan."
            ),
            next_appointment=next_appointment['full_datetime']
        ))

    # Treatment Plan Generation
    def generate_treatment_plan(self, patient_data: Dict[str, Any]):
        logger.info(f"Received patient data: {patient_data}")

        def validate_patient_data(patient_data: Dict[str, Any]) -> Dict[str, Any]:
            try:
                return {
                    'firstName': str(patient_data.get('firstName', 'Unknown')),
                    'lastName': str(patient_data.get('lastName', 'Unknown')),
                    'cdr_Score': float(patient_data['cdr_Score']),
                    'mmse_Score': float(patient_data['mmse_Score']),
                    'caregiver_Availability': str(patient_data.get('caregiverAvailability', 'Unknown'))
                }
            except (ValueError, TypeError, KeyError) as e:
                logger.error(f"Invalid patient data: {e}")
                raise ValueError("Invalid or missing critical data")

        try:
            # Validate patient data
            validated_data = validate_patient_data(patient_data)

            # Reset the expert system and declare facts
            self.reset()

            self.declare(PatientInfo(**validated_data))

            logger.info(f"Declared facts: {list(self.facts.values())}")

            # Run the rule engine
            self.run()

            logger.info(f"Facts after running rules: {list(self.facts.values())}")

            # Retrieve the treatment plan
            treatment_plan = None
            for current_fact in self.facts.values():
                if isinstance(current_fact, TreatmentPlan):
                    logger.info(f"TreatmentPlan object: {current_fact}")
                    treatment_plan = {
                        'first_name': validated_data['firstName'],
                        'last_name': validated_data['lastName'],
                        'dementia_level': current_fact.dementia_level.name,
                        'visit_frequency': current_fact.visit_frequency,
                        'treatment_recommendation': current_fact.treatment_recommendation,
                        'next_appointment': current_fact.next_appointment,
                    }
                    logger.info(f"TreatmentPlan: {treatment_plan}")
                    break

            if not treatment_plan:
                logger.error("No treatment plan generated")
                treatment_plan = {
                    'first_name': None,
                    'last_name': None,
                    'dementia_level': None,
                    'visit_frequency': None,
                    'treatment_recommendation': None,
                    'next_appointment': None,
                    'error': "No treatment plan generated"
                }

            return treatment_plan

        except ValueError as e:
            return {"error": str(e)}
