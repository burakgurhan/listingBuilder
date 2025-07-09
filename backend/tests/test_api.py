from unittest.mock import patch

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Backend is running. Use /api/v1 for API endpoints."}

def test_register_user(client):
    response = client.post(
        "/api/v1/register",
        json={"email": "newuser@example.com", "password": "newpassword", "confirmPassword": "newpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_register_user_password_mismatch(client):
    response = client.post(
        "/api/v1/register",
        json={"email": "another@example.com", "password": "password1", "confirmPassword": "password2"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Passwords do not match."}

def test_register_user_already_exists(client, test_user):
    # The 'test_user' fixture already created a user with this email
    response = client.post(
        "/api/v1/register",
        json={"email": test_user["email"], "password": "password", "confirmPassword": "password"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered."}

def test_login_user(client, test_user):
    response = client.post(
        "/api/v1/login",
        json=test_user,
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_login_user_invalid_credentials(client):
    response = client.post(
        "/api/v1/login",
        json={"email": "nouser@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials."}

def test_get_profile(client, auth_token, test_user_credentials):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/api/v1/profile", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_credentials["email"]
    assert "subscription" in data

def test_update_profile(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    new_email = "new_test@example.com"
    response = client.put(
        "/api/v1/profile",
        headers=headers,
        json={"email": new_email},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Profile updated successfully."
    assert data["email"] == new_email

@patch("app.routes.api.generate_listing")
def test_generate_text_and_history(mock_generate_listing, client, auth_token):
    # 1. Check that history is initially empty
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/api/v1/history", headers=headers)
    assert response.status_code == 200
    assert response.json() == []
 
    # 2. Mock the external call and generate text
    mock_data = {
        "title": "Generated Title",
        "description": "Generated Description",
        "bullet_points": ["Point 1", "Point 2"],
        "keywordsReport": "Keywords report content"
    }
    mock_generate_listing.return_value = mock_data
    
    gen_response = client.post(
        "/api/v1/generate_text",
        headers=headers,
        json={"url": "https://www.example.com"}
    )
    assert gen_response.status_code == 200
    gen_data = gen_response.json()
    assert gen_data["titles"] == [mock_data["title"]]
    assert gen_data["description"] == mock_data["description"]
    assert gen_data["bulletPoints"] == mock_data["bullet_points"]
    assert gen_data["keywordsReport"] == mock_data["keywordsReport"]
    mock_generate_listing.assert_called_once_with("https://www.example.com")

    # 3. Check history again to see the new item
    response = client.get("/api/v1/history", headers=headers)
    assert response.status_code == 200
    history_data = response.json()
    assert len(history_data) == 1
    history_item = history_data[0]
    assert history_item["title"] == "Generated Title"
    assert history_item["url"] == "https://www.example.com"
    assert history_item["status"] == "completed"
    item_id = history_item["id"]

    # 4. Delete the history item
    delete_response = client.delete(f"/api/v1/history/{item_id}", headers=headers)
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "History item deleted."}

    # 5. Check history one last time to ensure it's empty
    response = client.get("/api/v1/history", headers=headers)
    assert response.status_code == 200
    assert response.json() == []

def test_delete_nonexistent_history_item(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    delete_response = client.delete("/api/v1/history/9999", headers=headers)
    assert delete_response.status_code == 404
    assert delete_response.json() == {"detail": "History item not found."}

@patch("app.routes.api.send_reset_email")
def test_forgot_password(mock_send_reset_email, client, test_user):
    response = client.post(
        "/api/v1/forgot-password",
        json={"email": test_user["email"]},
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Password reset email sent successfully!"}
    mock_send_reset_email.assert_called_once()

def test_forgot_password_user_not_found(client):
    response = client.post(
        "/api/v1/forgot-password",
        json={"email": "nonexistent@example.com"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}