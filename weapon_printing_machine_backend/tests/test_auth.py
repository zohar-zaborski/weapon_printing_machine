# tests/test_auth.py
def test_user_registration(client, test_db):
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "id" in response.json()

