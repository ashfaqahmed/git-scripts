import os
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# GitLab Configuration
GITLAB_API_URL = "https://gitlab.com/api/v4"
PERSONAL_ACCESS_TOKEN = os.getenv("GITLAB_PERSONAL_ACCESS_TOKEN")

# JIRA Configuration
JIRA_API_URL = "https://myorg.atlassian.net/rest/api/latest"
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

GIT_HEADERS = {
    "Private-Token": PERSONAL_ACCESS_TOKEN
}

auth_string = f"{JIRA_USERNAME}:{JIRA_API_TOKEN}"
auth_token = base64.b64encode(auth_string.encode()).decode()
JIRA_HEADERS = {
    "Authorization": f"Basic {auth_token}",
    "Content-Type": "application/json"
}

if not PERSONAL_ACCESS_TOKEN or not JIRA_USERNAME or not JIRA_API_TOKEN:
    raise ValueError("Environment variables GITLAB_PERSONAL_ACCESS_TOKEN, JIRA_USERNAME, and JIRA_API_TOKEN must be set.")