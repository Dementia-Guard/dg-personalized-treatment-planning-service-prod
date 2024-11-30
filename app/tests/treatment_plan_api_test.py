from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_treatment_plan():
    # Define test input data
    payload = {
        "id": "patient123",
        "firstName": "John",
        "lastName": "Doe",
        "age": 65,
        "cdrScore": 1.5,
        "mmseScore": 20,
        "additionalNotes": "Difficulty with recent memory."
    }

    # Make a POST request to the API
    response = client.post("/api/treatment-plan/", json=payload)

    # Assert the response status code
    assert response.status_code == 200

    # Assert response data contains required fields
    response_data = response.json()
    assert response_data["fullName"] == "John Doe"
    assert response_data["dementia_level"] == "MILD"
    assert "treatment_recommendation" in response_data
    assert "next_appointment" in response_data


