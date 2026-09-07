"""Tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern"""


def test_get_all_activities(client, activities_with_participants):
    """
    ARRANGE: Activities fixture provides test data
    ACT: Request all activities
    ASSERT: Verify response structure and content
    """
    # Arrange
    expected_count = 3
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == expected_count
    assert "Empty Activity" in activities
    assert "Partial Activity" in activities
    assert "Full Activity" in activities


def test_activities_have_required_fields(client, activities_with_participants):
    """
    ARRANGE: Activities fixture provides test data
    ACT: Request all activities
    ASSERT: Verify each activity has required fields
    """
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert set(activity_data.keys()) == required_fields
        assert isinstance(activity_data["participants"], list)
        assert isinstance(activity_data["max_participants"], int)


def test_participants_are_emails(client, activities_with_participants):
    """
    ARRANGE: Activities fixture includes participants with emails
    ACT: Request all activities
    ASSERT: Verify participants are strings (emails)
    """
    # Arrange
    # (fixture provides activities with email strings)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant  # Basic email validation


def test_availability_count_calculation(client, activities_with_participants):
    """
    ARRANGE: Activities with known max and current participants
    ACT: Request all activities
    ASSERT: Verify availability calculation (max - current)
    """
    # Arrange
    expected_availability = {
        "Empty Activity": 5 - 0,      # 5 spots left
        "Partial Activity": 5 - 2,    # 3 spots left
        "Full Activity": 3 - 3        # 0 spots left
    }
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, expected_spots in expected_availability.items():
        actual_spots = activities[activity_name]["max_participants"] - len(activities[activity_name]["participants"])
        assert actual_spots == expected_spots
