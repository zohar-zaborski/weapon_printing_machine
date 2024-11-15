def test_create_customization(client, test_db, populate_weapons):
    response = client.post("/customize", json={
        "weapon_id": 1,
        "parts": [1, 2]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["weapon_id"] == 1
    assert data["parts"] == [1, 2]
    assert "print_job_id" in data


def test_get_all_customizations(client, test_db, populate_weapons):
    response = client.get("/customize")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
