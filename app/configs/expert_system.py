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
    NORMAL = auto()
    MILD = auto()
    MODERATE = auto()
    SEVERE = auto()


class PatientInfo(Fact):
    """Represents patient's medical information"""
    pass


class TreatmentPlan(Fact):
    dementia_level: DementiaLevel
    visit_frequency: int
    treatment_recommendation: str
    next_appointment: str

    def __init__(self, dementia_level: DementiaLevel, visit_frequency: int, treatment_recommendation: str, next_appointment: str):
        super().__init__()
        self.dementia_level = dementia_level
        self.visit_frequency = visit_frequency
        self.treatment_recommendation = treatment_recommendation
        self.next_appointment = next_appointment


class DementiaExpertSystem(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        # Initialize doctor availability management
        self.doctor_availability = DoctorAvailability()

    @Rule(PatientInfo(cdr_Score=P(lambda x: x == 0.0),
                      mmse_Score=P(lambda x: x >= 24.0)))
    def normal_dementia_level(self):
        """Rule for Normal Dementia Level"""
        logger.info("Normal dementia level rule triggered")  # Add debug log
        next_appointment = self.doctor_availability.find_next_available_slot('NORMAL')

        self.declare(TreatmentPlan(
            dementia_level=DementiaLevel.NORMAL,
            visit_frequency=180,
            treatment_recommendation="Continue current lifestyle. Annual cognitive screening.",
            next_appointment=next_appointment['full_datetime']
        ))

    @Rule(PatientInfo(cdr_Score=P(lambda x: 0.0 < x <= 1.0),
                      mmse_Score=P(lambda x: 19.0 <= x <= 23.0)))
    def mild_dementia_level(self):
        """Rule for Mild Dementia Level"""
        logger.info("Mild dementia level rule triggered")
        next_appointment = self.doctor_availability.find_next_available_slot('MILD')

        self.declare(TreatmentPlan(
            dementia_level=DementiaLevel.MILD,
            visit_frequency=90,  # Every 3 months
            treatment_recommendation="Begin mild cognitive exercise program. Consider memory aids.",
            next_appointment=next_appointment['full_datetime']
        ))

    @Rule(PatientInfo(cdr_Score=P(lambda x: 1.5 <= x <= 2.5),
                      mmse_Score=P(lambda x: 10.0 <= x <= 18.0)))
    def moderate_dementia_level(self):
        """Rule for Moderate Dementia Level"""
        logger.info("Moderate dementia level rule triggered")
        next_appointment = self.doctor_availability.find_next_available_slot('MODERATE')

        self.declare(TreatmentPlan(
            dementia_level=DementiaLevel.MODERATE,
            visit_frequency=60,  # Every 2 months
            treatment_recommendation="Recommend cognitive therapy. Assess need for medication.",
            next_appointment=next_appointment['full_datetime']
        ))

    @Rule(PatientInfo(cdr_Score=P(lambda x: x > 2.5),
                      mmse_Score=P(lambda x: x < 10.0)))
    def severe_dementia_level(self):
        """Rule for Severe Dementia Level"""
        logger.info("Severe dementia level rule triggered")
        next_appointment = self.doctor_availability.find_next_available_slot('SEVERE')

        self.declare(TreatmentPlan(
            dementia_level=DementiaLevel.SEVERE,
            visit_frequency=30,  # Monthly
            treatment_recommendation="Comprehensive care plan needed. Consider full-time care support.",
            next_appointment=next_appointment['full_datetime']
        ))

    def generate_treatment_plan(self, patient_data: Dict[str, Any]):
        logger.info(f"Received patient data: {patient_data}")

        def validate_patient_data(patient_data: Dict[str, Any]) -> Dict[str, Any]:
            try:
                return {
                    'firstName': str(patient_data.get('firstName', 'Unknown')),
                    'lastName': str(patient_data.get('lastName', 'Unknown')),
                    'cdr_Score': float(patient_data['cdr_Score']),
                    'mmse_Score': float(patient_data['mmse_Score'])
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
