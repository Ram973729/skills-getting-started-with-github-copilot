"""Integration tests for the Activity Management API endpoints.

Tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and preconditions
- Act: Execute the API call
- Assert: Verify the response and side effects
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestRootEndpoint:
    """Tests for the root endpoint GET /"""

    def test_root_redirects_to_index(self, client: TestClient):
        """
        Arrange: Create a test client
        Act: Make a GET request to /
        Assert: Verify it redirects to /static/index.html
        """
        # Arrange
        expected_redirect_url = "/static/index.html"

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert expected_redirect_url in response.headers["location"]


@pytest.mark.integration
class TestActivitiesEndpoint:
    """Tests for the GET /activities endpoint"""

    def test_get_all_activities_returns_200(self, client: TestClient):
        """
        Arrange: Client ready
        Act: GET /activities
        Assert: Status is 200 and response contains activities
        """
        # Arrange (implicit via client fixture)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) > 0

    def test_get_activities_returns_correct_structure(self, client: TestClient):
        """
        Arrange: Client ready
        Act: GET /activities
        Assert: Each activity has required fields
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_details in activities.items():
            assert isinstance(activity_name, str)
            assert required_fields.issubset(activity_details.keys())
            assert isinstance(activity_details["participants"], list)
            assert isinstance(activity_details["max_participants"], int)

    def test_get_activities_includes_all_activities(self, client: TestClient):
        """
        Arrange: Expected activity names
        Act: GET /activities
        Assert: All expected activities are present
        """
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for expected_activity in expected_activities:
            assert expected_activity in activities


@pytest.mark.integration
class TestSignupEndpoint:
    """Tests for the POST /activities/{activity_name}/signup endpoint"""

    def test_signup_new_student_success(self, client: TestClient, new_student_email: str):
        """
        Arrange: Prepare a new student email and existing activity
        Act: POST signup request for a student not yet in the activity
        Assert: Response is 200 and student is added to participants
        """
        # Arrange
        activity_name = "Chess Club"
        email = new_student_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]

    def test_signup_duplicate_student_fails(self, client: TestClient):
        """
        Arrange: Get an existing participant from an activity
        Act: Try to signup with that same email twice
        Assert: Second signup returns 400 Bad Request with appropriate message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club

        # Act - First signup (should work or be a duplicate already)
        response_first = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act - Second signup attempt
        response_second = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response_second.status_code == 400
        data = response_second.json()
        assert "detail" in data
        assert "already" in data["detail"].lower() or "signed up" in data["detail"].lower()

    def test_signup_nonexistent_activity_fails(self, client: TestClient, new_student_email: str):
        """
        Arrange: Prepare a request for a non-existent activity
        Act: POST signup request
        Assert: Response is 404 Not Found
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = new_student_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_valid_email_formats(self, client: TestClient):
        """
        Arrange: Prepare multiple valid email formats
        Act: POST signup requests with different email formats
        Assert: All are accepted (API doesn't validate email format)
        """
        # Arrange
        activity_name = "Programming Class"
        test_emails = [
            "user@example.com",
            "user.name@example.co.uk",
            "user+tag@example.com"
        ]

        # Act & Assert
        for email in test_emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            # Should either succeed or fail with 400 (if already registered)
            assert response.status_code in [200, 400]


@pytest.mark.integration
class TestDeleteParticipantEndpoint:
    """Tests for the DELETE /activities/{activity_name}/participants endpoint"""

    def test_delete_existing_participant_success(self, client: TestClient):
        """
        Arrange: Get an existing participant from an activity
        Act: DELETE request to remove that participant
        Assert: Response is 200 and participant is removed
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Existing participant

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]

    def test_delete_nonexistent_participant_fails(self, client: TestClient, new_student_email: str):
        """
        Arrange: Prepare a DELETE request for a participant not in the activity
        Act: DELETE request
        Assert: Response is 404 Not Found
        """
        # Arrange
        activity_name = "Chess Club"
        email = new_student_email  # Not in any activity

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_delete_from_nonexistent_activity_fails(self, client: TestClient, new_student_email: str):
        """
        Arrange: Prepare a DELETE request for a non-existent activity
        Act: DELETE request
        Assert: Response is 404 Not Found
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = new_student_email

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_delete_participant_updates_participant_list(self, client: TestClient):
        """
        Arrange: Get initial participant count
        Act: DELETE a participant, then GET activities
        Assert: Participant count is reduced by 1
        """
        # Arrange
        activity_name = "Gym Class"
        email = "john@mergington.edu"

        response_before = client.get("/activities")
        initial_count = len(response_before.json()[activity_name]["participants"])

        # Act
        response_delete = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response_delete.status_code == 200

        response_after = client.get("/activities")
        final_count = len(response_after.json()[activity_name]["participants"])
        assert final_count == initial_count - 1
        assert email not in response_after.json()[activity_name]["participants"]
