# Weather WebApp

<div align="center">
    <img src="./images/thunderCast.png" alt="DevOps Exercises" width="300">
</div>


A simple weather web app built with Python, using Flask, Nginx and Gunicorn.
CI/CD pipeline done with GitHub Actions.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Docker](#docker)
- [Continuous Integration](#continuous-integration)

## Features

- Check current weather conditions for any location.
- Built using Flask and Gunicorn for efficient handling of requests.
- Dockerized for easy deployment.
- Integrated security checks with Snyk and Gitleaks.
- Automated tests with pytest and linting with flake8 and pylint.

## Technologies Used

- Python 3.12
- Flask
- Gunicorn
- Docker
- GitHub Actions for CI/CD
- Snyk for security scanning
- Gitleaks for secret detection
- [API: open-meteo](https://api.open-meteo.com/v1/forecast)

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/niv-devops/weather-webapp.git
   cd weather-webapp
   ```

2. Active env, install dependencies, run application

   ```bash
   cd existing_repo
   . .venv/bin/activate
   pip install --break-system-packages --user <dependency>
   python3 weather.py
   ```

3. Install dependencies:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
   
4. Set up environment variables as needed (e.g., API keys for weather services).

## Usage

To run the application locally, use the following command:

```bash
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

You can then access the application at `http://localhost:5000`.

## Running Tests

To run the tests, execute:

```bash
pytest tests/
```

## Docker

To build and run the application using Docker, follow these steps:

1. Build the Docker image:
   ```bash
   docker build -t weather-webapp .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 weather-webapp
   ```

## Continuous Integration

This project uses GitHub Actions for CI/CD. The pipeline includes:

- Running tests and linting on every push and pull request.
- Building and pushing Docker images to GitHub Container Registry.
- Scanning for vulnerabilities using Snyk and Gitleaks.

### Pipeline Steps

1. **Test**: Runs all tests and checks for code quality.
2. **Build**: Builds the Docker image and pushes it to the GitHub Container Registry.
3. **Monitor**: Sends notifications to a Slack channel regarding the pipeline status.

***

# GitLab additional options

- [ ] [Edit README.md using makeareadme.com](https://www.makeareadme.com/)

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin http://3.122.61.221/niv/webapp.git
git branch -M main
git push -uf origin main
```

- [ ] [Set up project integrations](http://3.122.61.221/niv/webapp/-/settings/integrations)

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)
