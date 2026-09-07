"""Tests for DELETE /activities/{activity_name}/unregister endpoint using AAA pattern"""


def test_unregister_success(client, activities_with_participants):
    """
    ARRANGE: Partial activity with known participants
    ACT: Unregister a participant
    ASSERT: Response success, participant removed
    """
    # Arrange
    email = "alice@test.edu"  # In Partial Activity
    activity_name = "Partial Activity"
    initial_count = len(activities_with_participants[activity_name]["participants"])
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert: Response successful
    assert response.status_code == 200
    assert f"Unregistered {email} from {activity_name}" in response.json()["message"]
    
    # Assert: Participant removed from activity
    assert email not in activities_with_participants[activity_name]["participants"]
    assert len(activities_with_participants[activity_name]["participants"]) == initial_count - 1


def test_unregister_activity_not_found(client):
    """
    ARRANGE: Non-existent activity name
    ACT: Attempt to unregister
    ASSERT: 404 error returned
    """
    # Arrange
    email = "student@test.edu"
    activity_name = "Nonexistent Activity"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_not_signed_up(client, activities_with_participants):
    """
    ARRANGE: Partial activity, email not in participants
    ACT: Attempt to unregister someone not signed up
    ASSERT: 400 error, participants unchanged
    """
    # Arrange
    email = "notasignedupstudent@test.edu"
    activity_name = "Partial Activity"
    initial_participants = activities_with_participants[activity_name]["participants"].copy()
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert: Error response
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]
    
    # Assert: Participants unchanged
    assert activities_with_participants[activity_name]["participants"] == initial_participants


def test_resign_up_after_unregister(client, activities_with_participants):
    """
    ARRANGE: Partial activity with participant
    ACT: Unregister, then sign up the same email again
    ASSERT: Both operations successful, no errors
    """
    # Arrange
    email = "alice@test.edu"
    activity_name = "Partial Activity"
    
    # Act: Unregister
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert: Unregister successful
    assert unregister_response.status_code == 200
    assert email not in activities_with_participants[activity_name]["participants"]
    
    # Act: Re-sign up
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert: Re-signup successful
    assert signup_response.status_code == 200
    assert email in activities_with_participants[activity_name]["participants"]
