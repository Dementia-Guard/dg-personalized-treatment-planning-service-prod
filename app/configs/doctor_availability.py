from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json


class DoctorAvailability:
    def __init__(self):
        # Configurable availability with more detailed scheduling
        self._availability = {
            'Monday': [
                {'start': '09:00', 'end': '11:00', 'slots': 4, 'max_patients': 4},
                {'start': '14:00', 'end': '16:00', 'slots': 4, 'max_patients': 4}
            ],
            'Tuesday': [
                {'start': '10:00', 'end': '12:00', 'slots': 4, 'max_patients': 4},
                {'start': '15:00', 'end': '17:00', 'slots': 4, 'max_patients': 4}
            ],
            'Wednesday': [
                {'start': '09:30', 'end': '11:30', 'slots': 4, 'max_patients': 4},
                {'start': '14:30', 'end': '16:30', 'slots': 4, 'max_patients': 4}
            ],
            'Thursday': [
                {'start': '10:30', 'end': '12:30', 'slots': 4, 'max_patients': 4},
                {'start': '15:30', 'end': '17:30', 'slots': 4, 'max_patients': 4}
            ],
            'Friday': [
                {'start': '09:00', 'end': '11:00', 'slots': 4, 'max_patients': 4},
                {'start': '14:00', 'end': '16:00', 'slots': 4, 'max_patients': 4}
            ]
        }

        # Track current bookings
        self._current_bookings: Dict[str, List[Dict]] = {
            day: [] for day in self._availability.keys()
        }

    def find_next_available_slot(self,
                                 dementia_level: str,
                                 current_date: Optional[datetime] = None) -> Dict[str, str]:
        """
        Find the next available doctor's appointment slot

        Args:
            dementia_level (str): Patient's dementia level to prioritize scheduling
            current_date (datetime, optional): Starting date for slot search

        Returns:
            Dict with appointment details
        """
        if current_date is None:
            current_date = datetime.now()

        # Prioritization logic for appointment slots based on dementia level
        priority_order = {
            'NON_DEMENTED': 0,
            'VERY_MILD_DEMENTED': 1,
            'MILD_DEMENTED': 2,
            'MODERATE_DEMENTED': 3,
            'SEVERE_DEMENTED': 4
        }

        # Look ahead for 14 days to find an appropriate slot
        for days_ahead in range(14):
            test_date = current_date + timedelta(days=days_ahead)
            day_name = test_date.strftime('%A')

            # Check if the day is in our availability
            if day_name in self._availability:
                day_slots = self._availability[day_name]

                for slot in day_slots:
                    # Check if slot has available capacity
                    if len(self._current_bookings[day_name]) < slot['max_patients']:
                        # Book the slot
                        appointment_time = slot['start']
                        booking = {
                            'date': test_date.date(),
                            'day': day_name,
                            'time': appointment_time,
                            'dementia_level': dementia_level
                        }

                        self._current_bookings[day_name].append(booking)

                        return {
                            'date': test_date.strftime('%Y-%m-%d'),
                            'day': day_name,
                            'time': appointment_time,
                            'full_datetime': f"{test_date.strftime('%Y-%m-%d')} {appointment_time}"
                        }

        # If no slots found
        return {
            'date': 'N/A',
            'day': 'No Availability',
            'time': 'N/A',
            'full_datetime': 'No available slots found'
        }

    def get_availability_report(self) -> Dict:
        """
        Generate a report of current availability

        Returns:
            Dict with availability details
        """
        report = {}
        for day, slots in self._availability.items():
            report[day] = {
                'total_slots': sum(slot['max_patients'] for slot in slots),
                'booked_slots': len(self._current_bookings[day]),
                'availability_percentage': (1 - len(self._current_bookings[day]) / sum(
                    slot['max_patients'] for slot in slots)) * 100
            }
        return report

    def export_bookings(self) -> str:
        """
        Export current bookings to JSON

        Returns:
            JSON string of current bookings
        """
        return json.dumps(self._current_bookings, default=str)
