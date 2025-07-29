from fastapi.testclient import TestClient

def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Darwix AI Assignment API"}

# Add more integration tests for endpoints, e.g., test_get_calls
