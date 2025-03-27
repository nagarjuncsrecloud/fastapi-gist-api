from fastapi import FastAPI, HTTPException, Query
import requests
from functools import lru_cache
from typing import Optional

app = FastAPI()

GITHUB_API_URL = "https://api.github.com/users/{}/gists"

# Cache responses for 10 minutes
@lru_cache(maxsize=10)
def fetch_gists(username: str):
    """Fetch public gists for a GitHub user."""
    url = GITHUB_API_URL.format(username)
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="User not found or GitHub API error")

    return response.json()

@app.get("/{username}")
def get_user_gists(
    username: str,
    limit: int = Query(5, ge=1, le=100),
    offset: int = Query(0, ge=0),
    filter_descriptions: Optional[bool] = None
):
    """Fetch paginated and sorted gists for a user, with optional filtering."""
    gists = fetch_gists(username)

    # Sorting by created_at (newest first)
    gists.sort(key=lambda x: x["created_at"], reverse=True)

    # Replace empty descriptions with "No description"
    for gist in gists:
        if not gist.get("description"):
            gist["description"] = "No description"

    # Apply description filter if specified
    if filter_descriptions is not None:
        gists = [gist for gist in gists if (filter_descriptions and gist["description"] != "No description")]

    # Pagination
    paginated_gists = gists[offset:offset + limit]

    if not paginated_gists:
        return {"message": "No gists found"}

    return paginated_gists
