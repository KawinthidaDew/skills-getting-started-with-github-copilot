import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data

def test_signup_and_unregister():
    # Use a unique email to avoid conflicts
    activity = "Basketball Team"
    email = "pytestuser@mergington.edu"
    # Signup
    response = client.post(f"/activities/{activity}/signup", json={"email": email})
    assert response.status_code == 200 or response.status_code == 400  # 400 if already signed up
    # Unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200 or response.status_code == 404  # 404 if already removed

def test_signup_full_activity():
    activity = "Basketball Team"
    # Fill up the activity to its max (15)
    # 1 participant already exists, so add 14 more
    for i in range(2, 16):
        email = f"fulltest{i}@mergington.edu"
        client.post(f"/activities/{activity}/signup", json={"email": email})
    # Try to overfill
    response = client.post(f"/activities/{activity}/signup", json={"email": "overfill@mergington.edu"})
    assert response.status_code == 400
    assert "Activity is full" in response.text
