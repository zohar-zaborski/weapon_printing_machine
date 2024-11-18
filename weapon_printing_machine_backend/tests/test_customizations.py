# tests/test_weapons.py
def test_get_weapons(test_client):
    response = test_client.get("/weapons/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_weapon_by_id(test_client, db_session):
    # Add a weapon directly to the test database
    db_session.execute("INSERT INTO weapons (name, compatible_parts) VALUES ('Test Weapon', '1,2,3')")
    db_session.commit()
    response = test_client.get("/weapons/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Weapon"
