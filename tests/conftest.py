"""Pytest configuration and fixtures for FastAPI tests"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Fixture: FastAPI TestClient for making requests"""
    return TestClient(app)


@pytest.fixture
def activities_with_participants(monkeypatch):
    """Fixture: Mock activities with different participant states for testing"""
    mock_activities = {
        "Empty Activity": {
            "description": "Activity with no participants",
            "schedule": "Monday 3:00 PM",
            "max_participants": 5,
            "participants": []
        },
        "Partial Activity": {
            "description": "Activity with some participants",
            "schedule": "Tuesday 4:00 PM",
            "max_participants": 5,
            "participants": ["alice@test.edu", "bob@test.edu"]
        },
        "Full Activity": {
            "description": "Activity at maximum capacity",
            "schedule": "Wednesday 5:00 PM",
            "max_participants": 3,
            "participants": ["charlie@test.edu", "diana@test.edu", "eve@test.edu"]
        }
    }
    
    # Replace app's activities dict with mock for test isolation
    monkeypatch.setattr("src.app.activities", mock_activities)
    return mock_activities
