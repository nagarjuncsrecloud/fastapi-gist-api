<!-- ABOUT THE PROJECT -->
## About The Project
### HTTP API interacts with GitHub API to list Gist Users

Creates a simple HTTP web server API that interacts with the GitHub API and responds to requests on /<USER> with a list of the user’s publicly available Gists.

### Built With

* Python
* FastAPI
* Uvicorn
* Gist
* Docker CLI
* GitHub

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

* fastapi
* uvicorn
* requests
* redis
* pytest
* httpx
* pyyaml
* cookiecutter
* python-dotenv
* pytest-cookies

### How to build deploy and test in local

1. Find a Python project template on GitHub, e.g., cookiecutter-pypackage.

2. Clone the repository to get the minimal Python directory structure. Then copy the contents of the cloned cookiecutter package to your project workspace. Say, "fastapi-gist-api".
   ```sh
    git clone https://github.com/cookiecutter/cookiecutter-pypackage.git
    cd cookiecutter-pypackage
    cp -rp /path-to-cookiecutter-pypackage/* /path-to-workspace/fastapi-gist-api/
   ```

3. Create a requirements.txt to install the necesssary modules, packages necessary for the python application to run

fastapi
uvicorn
requests
redis
pytest
httpx
pyyaml
cookiecutter
python-dotenv
pytest-cookies

Install them using:
  ```sh
   pip install -r requirements.txt
  ```

4. Change git remote url to avoid accidental pushes to base project
  ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
  ```
5. Clone the project repository
  ```sh
   gh repo clone nagarjuncsrecloud/fastapi-gist-api
  ```
6. Automatically created a batch of gists using Python script "app/create_gists.py" with varying data and missing info to cover the test case scenarios. Make sure, not to add github token keys in the script to avoid any vulnerabilities. It is best to use it as environment variable and called in the script instead.
  ```python
   import requests
   import time

   # Replace with your GitHub Personal Access Token
   GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"

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
      ```

      Visit https://gist.github.com/ and check if all gists were created in your GitHub account. You can skip to Step-10.

7. Created app/main.py to fetch and display GitHub gists. Added an automated test tests/test_main.py for the same to cover all functionalities. 

* Support pagination (limit, offset)
* Filter gists based on description (with/without description)
* Cache responses for performance using lrucache
* Handling empty responses
* Prints the URLs of the created gists
* Handles API rate limits with a delay
* Write automated tests (pytest)

8. Created a Dockerfile to containerize the app by exposing docker on port 8080.

9. Created a GitHub Workflow File (./github/workflows/cicd.yml).

* Triggers on git push events
* Sets up Python & dependencies
* Builds and validates the FastAPI API
* Ensures the Docker container builds successfully along with the automated test using pytest
* Runs the tests after building the Docker image
* Ensures the test suite runs inside the container

Benefits of This Approach

* Uses TestClient from fastapi.testclient (lightweight, fast, no need for external requests).
* Tests run during docker build, ensuring a valid API
* GitHub Actions CI/CD pipeline automates testing
* If tests fail, the Docker build stops, preventing bad deployments
* Ensures valid JSON responses and correct data handling.

10. Test Locally Before Pushing
Before pushing to GitHub, test everything locally:
```sh
 # Run tests outside Docker
 pytest tests/

 # Build and run the Docker container
 docker build -t fastapi-gist-api .
 docker run -d -p 8080:8080 --name fastapi-container fastapi-gist-api

 # Run tests inside the running container
 docker exec fastapi-container pytest tests/
```
This ensures the FastAPI application is running inside a Docker container on port 8080.

11. Test the API Locally Using HTTP Requests using cURL or PostMan
```sh
 curl -X GET "http://127.0.0.1:8080/octocat"
 curl -X GET "http://127.0.0.1:8080/nagarjuncsrecloud"

 # Get 5 gists (default) from page 1 (offset 0)
 curl -X GET "http://127.0.0.1:8080/octocat?limit=5&offset=0"

 # Get 10 gists from page 2 (offset 10)
 curl -X GET "http://127.0.0.1:8080/octocat?limit=10&offset=10"

 # Get only 3 gists from the start
 curl -X GET "http://127.0.0.1:8080/octocat?limit=3&offset=0"

 # Test API with an invalid user (expect a 404 response)
 curl -X GET "http://127.0.0.1:8080/unknownuser"

 # Get only 2 gists from the start for user nagarjuncsrecloud
 curl -X GET "http://127.0.0.1:8080/nagarjuncsrecloud?limit=2&offset=0"
```

12. Test via http://127.0.0.1:8080 in Browser or Postman
    Open your browser and visit:
        http://127.0.0.1:8080/octocat?limit=5&offset=0
    You should see a list of GitHub gists.

13. Run Tests Inside the Docker Container
```sh
 # Step 1: Execute tests inside the running Docker container
 docker exec fastapi-container pytest tests/
```
This runs pytest inside the Docker container to validate the API.

14. Stop and Restart the Application
```sh
 # Stop the running container
 docker stop fastapi-container

 # Remove the container
 docker rm fastapi-container

 # Start a new container
 docker run -d -p 8080:8080 --name fastapi-container fastapi-gist-api
```
This ensures you’re always testing with a fresh container.

15. Push Code to GitHub and Trigger the CI/CD Pipeline
```sh
 # Step 1: Initialize Git Repository (If not already done)
 git init

 # Step 2: Add all files to Git
 git add .

 # Step 3: Commit the changes
 git commit -m "Initial commit with FastAPI GitHub Gist API"

 # Step 4: Create a GitHub Repository (if not created)
 # Go to GitHub and create a new repository, then copy the URL

 # Step 5: Add the GitHub remote repository
 git remote add origin https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY.git

 # Step 6: Push the code to GitHub (this triggers CI/CD)
 git push -u origin main
```

16. Verify the CI/CD Pipeline Execution on GitHub
   Go to your GitHub repository. -> Click on the "Actions" tab. 
You should see the workflow running automatically on push.
