"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern"""


def test_signup_success(client, activities_with_participants):
    """
    ARRANGE: Empty activity fixture, new email
    ACT: Sign up for activity
    ASSERT: Response success, participant added to activity
    """
    # Arrange
    email = "newstudent@test.edu"
    activity_name = "Empty Activity"
    initial_count = len(activities_with_participants[activity_name]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert: Response successful
    assert response.status_code == 200
    assert f"Signed up {email} for {activity_name}" in response.json()["message"]
    
    # Assert: Participant added to activity
    assert email in activities_with_participants[activity_name]["participants"]
    assert len(activities_with_participants[activity_name]["participants"]) == initial_count + 1


def test_signup_activity_not_found(client):
    """
    ARRANGE: Non-existent activity name
    ACT: Attempt to sign up
    ASSERT: 404 error returned
    """
    # Arrange
    email = "student@test.edu"
    activity_name = "Nonexistent Activity"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_duplicate_email(client, activities_with_participants):
    """
    ARRANGE: Partial activity with existing participants
    ACT: Attempt to sign up with email already in activity
    ASSERT: 400 error, participant not duplicated
    """
    # Arrange
    email = "alice@test.edu"  # Already in Partial Activity
    activity_name = "Partial Activity"
    initial_count = len(activities_with_participants[activity_name]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert: Error response
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    
    # Assert: No duplicate added
    assert activities_with_participants[activity_name]["participants"].count(email) == 1
    assert len(activities_with_participants[activity_name]["participants"]) == initial_count


def test_signup_empty_email(client, activities_with_participants):
    """
    ARRANGE: Empty email string
    ACT: Attempt to sign up with empty email
    ASSERT: API accepts (no validation), adds to activity
    """
    # Arrange
    email = ""
    activity_name = "Empty Activity"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert: Backend accepts empty string (current behavior)
    assert response.status_code == 200
    assert email in activities_with_participants[activity_name]["participants"]
