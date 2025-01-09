from utils.helper import (
    fetch_open_merge_requests,
    extract_jira_key,
    get_jira_ticket_status_and_author,
    close_merge_request,
    add_comment_to_merge_request,
    check_merge_request_conflicts,
    log_message,
)

# List of target authors
TARGET_AUTHORS = ["john.doe", "jane.smith", "dev.user"]

def process_open_merge_requests():
    """
    Process open MRs from specific authors, check Jira tickets, and perform actions.
    """
    repository_names = [
        "example_org/project_a",
        "example_org/project_b"
    ]

    log_message("Fetching open merge requests...")
    open_mrs = fetch_open_merge_requests(repository_names)

    for mr in open_mrs:
        project_id = mr.get("project_id")
        mr_iid = mr.get("iid")
        mr_link = mr.get("web_url", "")
        author_username = mr.get("author", {}).get("username")
        title = mr.get("title", "")
        description = mr.get("description", "")

        log_message(f"Processing MR {mr_iid} by {author_username}...")

        if author_username not in TARGET_AUTHORS:
            continue

        jira_key = extract_jira_key(title, description)
        if not jira_key:
            log_message(f"No Jira key found for MR {mr_iid}. Skipping...")
            continue

        jira_status, _, _ = get_jira_ticket_status_and_author(jira_key)

        if jira_status == "Closed":
            close_merge_request(
                project_id,
                mr_iid,
                comment=f"Jira ticket {jira_key} is already closed. Closing this MR."
            )
            log_message(f"Closed MR {mr_link} as the associated Jira ticket {jira_key} is closed.")
        else:
            has_conflicts, _, _, _, _, _ = check_merge_request_conflicts(project_id, mr_iid)

            if has_conflicts:
                add_comment_to_merge_request(
                    project_id,
                    mr_iid,
                    comment=f"@{author_username}, please resolve the merge conflicts so this MR can be merged."
                )
            else:
                log_message(f"MR {mr_link} has no conflicts but the Jira ticket {jira_key} is not closed.")

if __name__ == "__main__":
    process_open_merge_requests()