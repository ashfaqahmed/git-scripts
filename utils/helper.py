import requests
import re
from datetime import datetime, timedelta, timezone
from config import GITLAB_API_URL, GIT_HEADERS, JIRA_API_URL, JIRA_HEADERS

# Log collection
logs = []

actions_performed = False

def log_message(message):
    """
    Log a message and store it for email.
    """
    print(" - " + message + "\n")
    logs.append(" - " + message + "\n")

def fetch_open_merge_requests(repository_names):
    """
    Fetch all open merge requests for specific repositories.

    :param repository_names: List of repository names to fetch MRs for.
    :return: List of open merge requests for the specified repositories.
    """
    all_open_mrs = []

    for repo_name in repository_names:
        # Fetch the project details to get the project ID
        project_url = f"{GITLAB_API_URL}/projects/{requests.utils.quote(repo_name, safe='')}"
        project_response = requests.get(project_url, headers=GIT_HEADERS)

        if project_response.status_code == 200:
            project_id = project_response.json()["id"]
            log_message(f"Fetching MRs for repository: {repo_name}")

            # Fetch open merge requests for the project
            mr_url = f"{GITLAB_API_URL}/projects/{project_id}/merge_requests"
            params = {"state": "opened", "per_page": 200}
            response = requests.get(mr_url, headers=GIT_HEADERS, params=params)

            if response.status_code == 200:
                open_mrs = response.json()
                log_message(f"Found {len(open_mrs)} open MRs in repository: {repo_name}")
                all_open_mrs.extend(open_mrs)
            else:
                log_message(f"Failed to fetch MRs for {repo_name}: {response.status_code} - {response.text}")
        else:
            log_message(
                f"Failed to fetch project details for {repo_name}: {project_response.status_code} - {project_response.text}")

    return all_open_mrs

def add_comment_to_merge_request(project_id, merge_request_iid, comment):
    """
    Add a comment to a merge request only if the comment doesn't already exist.
    """
    global actions_performed

    url = f"{GITLAB_API_URL}/projects/{project_id}/merge_requests/{merge_request_iid}/notes"
    data = {"body": comment}
    response = requests.post(url, headers=GIT_HEADERS, json=data)

    if response.status_code == 201:
        log_message(f"Comment added to MR {merge_request_iid}.")
        actions_performed = True
    else:
        log_message(f"Failed to add comment to MR {merge_request_iid}: {response.status_code} - {response.text}")

def close_merge_request(project_id, merge_request_iid, comment):
    """
    Close a merge request by adding a comment and then closing it.
    """
    global actions_performed

    # Add a comment to the merge request
    add_comment_to_merge_request(project_id, merge_request_iid, comment)

    # Close the merge request
    url = f"{GITLAB_API_URL}/projects/{project_id}/merge_requests/{merge_request_iid}"
    data = {"state_event": "close"}
    response = requests.put(url, headers=GIT_HEADERS, json=data)

    if response.status_code == 200:
        actions_performed = True
        log_message(f"Successfully closed MR {merge_request_iid} in project {project_id}.")
    else:
        log_message(f"Failed to close MR {merge_request_iid}: {response.status_code} - {response.text}")

def check_merge_request_conflicts(project_id, merge_request_iid):
    """
    Check if a merge request has conflicts and fetch its details.
    """
    url = f"{GITLAB_API_URL}/projects/{project_id}/merge_requests/{merge_request_iid}"
    response = requests.get(url, headers=GIT_HEADERS)

    if response.status_code == 200:
        data = response.json()
        has_conflicts = data.get("has_conflicts", True)
        return has_conflicts
    else:
        log_message(f"Failed to check merge request conflicts: {response.status_code} - {response.text}")
        return True

def extract_jira_key(title, description):
    """
    Extract the JIRA key from the title or description.
    """
    jira_key_pattern = r"[A-Z]+-\d+"  # Regex pattern for JIRA keys like PROJECT-123
    match = re.search(jira_key_pattern, f"{title} {description}")
    return match.group(0) if match else None

def get_jira_ticket_status_and_author(jira_key):
    """
    Fetch the status of a JIRA ticket and the author's details.
    """
    url = f"{JIRA_API_URL}/issue/{jira_key}"
    response = requests.get(url, headers=JIRA_HEADERS)

    if response.status_code == 200:
        data = response.json()
        status = data.get("fields", {}).get("status", {}).get("name", "Unknown")
        creator_display_name = data.get("fields", {}).get("creator", {}).get("displayName", "Unknown")
        creator_account_id = data.get("fields", {}).get("creator", {}).get("accountId", "Unknown")
        return status, creator_display_name, creator_account_id
    else:
        log_message(f"Failed to fetch JIRA ticket: {response.status_code} - {response.text}")
        return "Unknown", "Unknown", "Unknown"