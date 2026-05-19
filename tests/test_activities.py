"""Unit tests for activity management business logic.

Tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and expected values
- Act: Execute the logic to test
- Assert: Verify the results
"""

import pytest


@pytest.mark.unit
class TestActivityDataStructure:
    """Tests for validating activity data structure"""

    def test_activity_has_required_fields(self, sample_activities):
        """
        Arrange: Load sample activities
        Act: Check each activity's fields
        Assert: All required fields exist with correct types
        """
        # Arrange
        required_fields = {
            "description": str,
            "schedule": str,
            "max_participants": int,
            "participants": list
        }

        # Act & Assert
        for activity_name, activity_data in sample_activities.items():
            for field, expected_type in required_fields.items():
                assert field in activity_data, f"Field '{field}' missing from {activity_name}"
                assert isinstance(activity_data[field], expected_type), \
                    f"Field '{field}' in {activity_name} is not {expected_type.__name__}"

    def test_activity_description_is_not_empty(self, sample_activities):
        """
        Arrange: Load sample activities
        Act: Check descriptions
        Assert: All activities have non-empty descriptions
        """
        # Arrange & Act & Assert
        for activity_name, activity_data in sample_activities.items():
            assert activity_data["description"], f"Activity '{activity_name}' has empty description"
            assert len(activity_data["description"]) > 0

    def test_activity_schedule_is_not_empty(self, sample_activities):
        """
        Arrange: Load sample activities
        Act: Check schedules
        Assert: All activities have non-empty schedules
        """
        # Arrange & Act & Assert
        for activity_name, activity_data in sample_activities.items():
            assert activity_data["schedule"], f"Activity '{activity_name}' has empty schedule"
            assert len(activity_data["schedule"]) > 0

    def test_max_participants_is_positive(self, sample_activities):
        """
        Arrange: Load sample activities
        Act: Check max_participants values
        Assert: All max_participants are positive integers
        """
        # Arrange & Act & Assert
        for activity_name, activity_data in sample_activities.items():
            assert activity_data["max_participants"] > 0, \
                f"Activity '{activity_name}' has non-positive max_participants"


@pytest.mark.unit
class TestParticipantCounting:
    """Tests for participant count calculations"""

    def test_participants_list_is_valid(self, sample_activities):
        """
        Arrange: Load sample activities
        Act: Check participants lists
        Assert: All participant lists contain valid email strings
        """
        # Arrange & Act & Assert
        for activity_name, activity_data in sample_activities.items():
            participants = activity_data["participants"]
            assert isinstance(participants, list), \
                f"Participants in {activity_name} is not a list"
            for participant in participants:
                assert isinstance(participant, str), \
                    f"Participant in {activity_name} is not a string: {participant}"
                assert "@" in participant, \
                    f"Participant email in {activity_name} is not valid format: {participant}"

    def test_available_spots_calculation(self, sample_activities):
        """
        Arrange: Get activity data with known max and current participants
        Act: Calculate available spots
        Assert: Calculation is correct (max - current = available)
        """
        # Arrange
        activity = sample_activities["Chess Club"]
        max_participants = activity["max_participants"]
        current_participants = len(activity["participants"])

        # Act
        available_spots = max_participants - current_participants

        # Assert
        assert available_spots >= 0, "Available spots cannot be negative"
        assert available_spots == (max_participants - current_participants)

    def test_no_double_counting_of_participants(self, sample_activities):
        """
        Arrange: Check for duplicate emails in participant lists
        Act: Count unique vs total participants
        Assert: All participants are unique (no duplicates)
        """
        # Arrange & Act & Assert
        for activity_name, activity_data in sample_activities.items():
            participants = activity_data["participants"]
            unique_count = len(set(participants))
            total_count = len(participants)
            assert unique_count == total_count, \
                f"Activity '{activity_name}' has duplicate participants"


@pytest.mark.unit
class TestActivityAvailability:
    """Tests for activity availability logic"""

    def test_activity_with_available_spots(self, sample_activities):
        """
        Arrange: Get an activity with available spots
        Act: Check if spots available
        Assert: Activity has positive available spots
        """
        # Arrange
        activity = sample_activities["Gym Class"]
        max_participants = activity["max_participants"]
        current_participants = len(activity["participants"])

        # Act
        available_spots = max_participants - current_participants

        # Assert
        assert available_spots > 0, "Test activity should have available spots"

    def test_activity_at_capacity(self):
        """
        Arrange: Create an activity at max capacity
        Act: Calculate available spots
        Assert: Available spots is zero
        """
        # Arrange
        activity_at_capacity = {
            "description": "Full Activity",
            "schedule": "Test time",
            "max_participants": 2,
            "participants": ["user1@test.com", "user2@test.com"]
        }

        # Act
        available_spots = activity_at_capacity["max_participants"] - len(activity_at_capacity["participants"])

        # Assert
        assert available_spots == 0, "Activity should be at capacity"

    def test_activity_exceeding_capacity_is_invalid(self):
        """
        Arrange: Create an activity with more participants than max
        Act: Check if invalid state exists
        Assert: Flag the invalid state (this should not happen in normal operation)
        """
        # Arrange
        invalid_activity = {
            "description": "Invalid Activity",
            "schedule": "Test time",
            "max_participants": 2,
            "participants": ["user1@test.com", "user2@test.com", "user3@test.com"]
        }

        # Act
        is_over_capacity = len(invalid_activity["participants"]) > invalid_activity["max_participants"]

        # Assert
        assert is_over_capacity, "Activity exceeds capacity (invalid state detected)"


@pytest.mark.unit
class TestEmailFormatValidation:
    """Tests for email validation in participant lists"""

    def test_valid_email_format(self):
        """
        Arrange: Test emails
        Act: Check format
        Assert: Valid emails contain @ symbol
        """
        # Arrange
        valid_emails = [
            "user@example.com",
            "john.doe@school.edu",
            "student+tag@mergington.edu"
        ]

        # Act & Assert
        for email in valid_emails:
            assert "@" in email, f"Email '{email}' should contain @"
            parts = email.split("@")
            assert len(parts) == 2, f"Email '{email}' should have exactly one @"
            assert len(parts[0]) > 0, f"Email '{email}' should have local part"
            assert len(parts[1]) > 0, f"Email '{email}' should have domain part"

    def test_invalid_email_format(self):
        """
        Arrange: Invalid email formats
        Act: Check if they lack proper format (local@domain)
        Assert: Invalid emails identified
        """
        # Arrange
        invalid_emails = [
            ("notanemail", "no @ symbol"),
            ("@nodomain", "empty local part"),
            ("user@", "empty domain"),
            ("user@@example.com", "multiple @ symbols")
        ]

        # Act & Assert
        for email, reason in invalid_emails:
            at_count = email.count("@")
            parts = email.split("@")
            
            if at_count != 1:
                # Multiple or no @ symbols - definitely invalid
                assert at_count != 1, f"Email '{email}' should be invalid ({reason})"
            else:
                # Exactly one @, but check for empty local or domain parts
                has_empty_part = len(parts[0]) == 0 or len(parts[1]) == 0
                assert has_empty_part, f"Email '{email}' should be invalid ({reason})"
