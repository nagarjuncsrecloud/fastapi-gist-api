from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_fetch_gists():
    """Test fetching gists for a sample user (octocat)."""
    response = client.get("/octocat?limit=3&offset=0")
    assert response.status_code == 200
    json_response = response.json()
    assert isinstance(json_response, list)  # Ensure we get a list of gists

def test_pagination():
    """Test pagination works correctly."""
    response = client.get("/octocat?limit=5&offset=10")
    assert response.status_code == 200
    json_response = response.json()
    
    # Ensure response is either a list or a valid error message
    if isinstance(json_response, dict) and "message" in json_response:
        assert json_response["message"] in ["No gists found"]
    else:
        assert isinstance(json_response, list)  

def test_empty_response():
    """Test handling empty responses gracefully."""
    response = client.get("/unknownuser")
    json_response = response.json()
    
    # Some APIs return 404, others return 200 with an error message
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert "message" in json_response and json_response["message"] in ["User not found", "No gists found"]

def test_filter_gists_with_description():
    """Test filtering gists to only include those with descriptions."""
    response = client.get("/octocat?filter_descriptions=true")
    assert response.status_code == 200
    json_response = response.json()
    
    # Ensure response is a list before filtering
    if isinstance(json_response, list):
        assert all("description" in gist and gist["description"] != "No description" for gist in json_response)
    else:
        assert "message" in json_response  # Handle cases where no gists are found

def test_filter_gists_without_description():
    """Test filtering gists to only include those without descriptions."""
    response = client.get("/octocat?filter_descriptions=false")
    assert response.status_code == 200
    json_response = response.json()

    # Ensure response is a list before filtering
    if isinstance(json_response, list):
        assert all("description" in gist and gist["description"] == "No description" for gist in json_response)
    else:
        assert "message" in json_response  # Handle cases where no gists are found
