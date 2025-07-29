from fastapi.testclient import TestClient

def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Darwix AI Assignment API"}

def test_get_calls(client: TestClient):
    response = client.get("/api/v1/calls?limit=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# Add more integration tests for endpoints, e.g., test_get_calls
