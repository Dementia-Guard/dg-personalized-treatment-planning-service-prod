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
                "1. Annual cognitive screenings using multiple tools (MMSE, MoCA).",
                "2. Mediterranean diet, regular aerobic exercise (150 min/week), cognitive stimulation.",
                "3. Manage vascular risk factors (hypertension, diabetes, cholesterol) and avoid smoking/excessive alcohol.",
                "4. Establish cognitive baseline and educate on early warning signs of cognitive decline."
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
                "1. Annual cognitive screenings using multiple assessment tools (MMSE, MoCA).",
                "2. Suggest patient join cognitive stimulation groups and social activities.",
                "3. Optimize management of medical conditions that may affect cognition.",
                "4. Discuss advance care planning while decision-making capacity is intact."
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
                "1. Implement structured cognitive exercises and memory training (20-30 min daily).",
                "2. Train caregivers in communication techniques and early dementia management.",
                "3. Consider cholinesterase inhibitors if symptoms progress.",
                "4. Schedule hearing/vision assessment and optimize sensory function.",
                "5. Maintain social engagement and meaningful activities with caregiver support."
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
                "1. Engage in community-based cognitive stimulation programs (2-3 times weekly).",
                "2. Connect with local dementia support services and caregiver resources.",
                "3. Implement memory aids and reminder systems in the home environment.",
                "4. Establish medication management system and evaluate transportation needs.",
                "5. Consider technological solutions for remote monitoring and support."
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
                "1. Initiate cholinesterase inhibitors (donepezil, rivastigmine, or galantamine).",
                "2. Implement comprehensive memory aids, calendars, and structured daily routines.",
                "3. Caregiver training on managing emerging behavioral symptoms and communication strategies.",
                "4. Home safety assessment and modifications to prevent falls and wandering.",
                "5. Begin discussions about advance directives and long-term care planning."
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
                "1. Initiate medication therapy with close monitoring for adherence and side effects.",
                "2. Arrange visiting nurse or home care services (2-3 times weekly) for medication management.",
                "3. Connect with adult day programs specializing in dementia care.",
                "4. Install home monitoring systems and medication reminder technology.",
                "5. Evaluate capacity for independent living and explore supportive housing options."
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
                "1. Optimize pharmacological management: cholinesterase inhibitors and consider memantine.",
                "2. Implement non-pharmacological approaches for behavioral symptoms (redirection, routine).",
                "3. Caregiver training on managing activities of daily living and preventing caregiver burnout.",
                "4. Assess and treat co-morbid conditions that may worsen cognition or function.",
                "5. Evaluate need for assistive devices, home modifications, and respite care services."
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
                "1. Arrange comprehensive home care services or consider assisted living placement.",
                "2. Implement medication management system with professional oversight.",
                "3. Establish guardianship or power of attorney if not already in place.",
                "4. Coordinate multidisciplinary care team (geriatrics, neurology, social work).",
                "5. Implement fall prevention strategies and regular nutrition assessment."
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
                "1. Focus on comfort care and quality of life measures rather than cognitive enhancement.",
                "2. Provide caregiver training on late-stage dementia care, including feeding techniques.",
                "3. Address common complications: infection prevention, skin care, pain management.",
                "4. Consider palliative care consultation and discuss goals of care.",
                "5. Evaluate medication appropriateness and discontinue unnecessary treatments."
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
                "1. Facilitate placement in specialized memory care or skilled nursing facility.",
                "2. Implement palliative care approach focused on comfort and dignity.",
                "3. Establish clear advance directives regarding hospitalization and life-sustaining treatments.",
                "4. Create sensory stimulation program tailored to remaining abilities.",
                "5. Coordinate care conferences with facility staff and any involved family members."
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
