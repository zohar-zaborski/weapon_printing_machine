# tests/test_auth.py
def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "email": "testuser@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"


def test_login_user(client, test_db):
    client.post(
        "/auth/register",
        json={"username": "testuser", "email": "testuser@example.com", "password": "password123"}
    )
    response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
