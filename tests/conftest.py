"""Shared test fixtures and configuration for the activity management API tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app
import src.app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture: Automatically reset activities to initial state before each test.
    
    This ensures test isolation by resetting the shared in-memory database.
    The autouse=True makes this fixture run before every test automatically.
    """
    # Setup: Initialize activities with fresh test data
    app_module.activities = {
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
        "Soccer Team": {
            "description": "Join the school soccer team for practices and matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 18,
            "participants": ["alex@mergington.edu", "maria@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Practice basketball skills and play friendly games",
            "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["jordan@mergington.edu", "taylor@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore drawing, painting, and mixed media art projects",
            "schedule": "Mondays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["harper@mergington.edu", "liam@mergington.edu"]
        },
        "Drama Society": {
            "description": "Rehearse scenes and prepare performances for school events",
            "schedule": "Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["ava@mergington.edu", "noah@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Wednesdays, 4:30 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["sophia@mergington.edu", "ethan@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Prepare for science competitions and solve challenging problems",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["mia@mergington.edu", "lucas@mergington.edu"]
        }
    }
    
    # Yield control to the test
    yield
    
    # Teardown: Activities are automatically reset on next test via setup


@pytest.fixture
def client():
    """
    Fixture: Provides a TestClient for making requests to the FastAPI application.
    
    This client is used to test all API endpoints in an isolated environment.
    """
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """
    Fixture: Provides sample activity data for use in tests.
    
    Returns a dictionary with activity names as keys and activity details as values.
    Each test gets a fresh copy of this data to avoid test interdependencies.
    """
    return {
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
        }
    }


@pytest.fixture
def test_student_email():
    """Fixture: Provides a test student email address for signup tests."""
    return "test.student@mergington.edu"


@pytest.fixture
def new_student_email():
    """Fixture: Provides a new student email address for unregistered student tests."""
    return "newstudent@mergington.edu"


# Pytest markers for organizing tests
def pytest_configure(config):
    """Register custom pytest markers."""
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
