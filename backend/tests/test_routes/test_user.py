def test_create_user(client):
    data = {"email":"ping@fastapi.vom", "password":"supersecret"}
    response = client.post("/users/", json=data)
    assert response.status_code==201
    assert response.json()["email"] == "ping@fastapi.vom"