# tests/test_auth.py
def test_user_registration(client, test_db):
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "id" in response.json()

def test_user_login(client, test_db):
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
