import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data

def test_signup_for_activity_success():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Ensure user is not already signed up
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    # Clean up
    activities[activity]["participants"].remove(email)

def test_signup_for_activity_duplicate():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Add user first
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    # Clean up
    activities[activity]["participants"].remove(email)

def test_signup_for_activity_not_found():
    response = client.post("/activities/NonexistentActivity/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
