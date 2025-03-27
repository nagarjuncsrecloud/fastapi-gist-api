import requests
import time

# Replace with your GitHub Personal Access Token
GITHUB_TOKEN = "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"

# GitHub API URL for creating gists
GITHUB_API_URL = "https://api.github.com/gists"

# Headers with authentication
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# List of gists to be created (17 gists with mixed descriptions)
gist_payloads = [
    {"description": f"Gist {i+1} - Example Code" if i % 2 == 0 else "", "public": True, 
     "files": {f"file{i+1}.txt": {"content": f"This is the content of Gist {i+1}"}}}
    for i in range(17)
]

# Create gists
for index, gist in enumerate(gist_payloads):
    response = requests.post(GITHUB_API_URL, json=gist, headers=HEADERS)
    
    if response.status_code == 201:
        print(f"Created Gist {index+1}: {response.json()['html_url']}")
    else:
        print(f"Failed to create Gist {index+1}: {response.json()}")

    # Avoid rate limiting by adding a small delay (optional)
    time.sleep(1)
