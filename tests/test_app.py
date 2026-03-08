import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Create a test client
client = TestClient(app)

# Original activities data for resetting
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball league and practice",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn tennis skills and play matches",
        "schedule": "Wednesdays and Saturdays, 3:00 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "lily@mergington.edu"]
    },
    "Drama Club": {
        "description": "Perform in plays and develop acting skills",
        "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["sarah@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and sculpture",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["grace@mergington.edu", "lucas@mergington.edu"]
    },
    "Debate Team": {
        "description": "Compete in debates and develop argumentation skills",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["noah@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 22,
        "participants": ["ava@mergington.edu", "ethan@mergington.edu"]
    }
}

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the activities dictionary before each test"""
    activities.clear()
    activities.update(ORIGINAL_ACTIVITIES)


class TestActivitiesAPI:
    """Test suite for the activities API endpoints"""

    def test_get_activities_success(self):
        """Test GET /activities returns all activities with correct structure"""
        # Arrange - activities are reset by fixture

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 9  # All activities present

        # Check structure of one activity
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)

    def test_signup_success(self):
        """Test successful signup for an activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

        # Verify participant was added
        get_response = client.get("/activities")
        activities_data = get_response.json()
        assert email in activities_data[activity_name]["participants"]

    def test_signup_activity_not_found(self):
        """Test signup for non-existent activity returns 404"""
        # Arrange
        invalid_activity = "NonExistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(f"/activities/{invalid_activity}/signup?email={email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_email(self):
        """Test signup with email already registered returns 400"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in participants

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]

    def test_unregister_success(self):
        """Test successful unregister from an activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered

        # Act
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

        # Verify participant was removed
        get_response = client.get("/activities")
        activities_data = get_response.json()
        assert email not in activities_data[activity_name]["participants"]

    def test_unregister_activity_not_found(self):
        """Test unregister from non-existent activity returns 404"""
        # Arrange
        invalid_activity = "NonExistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(f"/activities/{invalid_activity}/unregister?email={email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_unregister_email_not_registered(self):
        """Test unregister with email not registered returns 400"""
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"  # Not in participants

        # Act
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"]