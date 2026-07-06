from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities_returns_all_activities():
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert expected_activity in payload
    assert "description" in payload[expected_activity]
    assert "participants" in payload[expected_activity]


def test_signup_adds_participant_and_returns_success_message():
    # Arrange
    activity_name = "Chess Club"
    test_email = "unit-test-user@mergington.edu"
    if test_email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(test_email)

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={test_email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {test_email} for {activity_name}"}
    assert test_email in activities[activity_name]["participants"]


def test_signup_duplicate_participant_returns_400():
    # Arrange
    activity_name = "Chess Club"
    test_email = "duplicate-test@mergington.edu"
    if test_email not in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].append(test_email)

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={test_email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant_returns_success_message():
    # Arrange
    activity_name = "Chess Club"
    test_email = "remove-test@mergington.edu"
    if test_email not in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].append(test_email)

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{test_email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {test_email} from {activity_name}"}
    assert test_email not in activities[activity_name]["participants"]


def test_remove_missing_participant_returns_404():
    # Arrange
    activity_name = "Chess Club"
    missing_email = "missing-test@mergington.edu"
    if missing_email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(missing_email)

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{missing_email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
