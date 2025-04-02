# GitLab Merge Request Cleanup Tool

A powerful Python script that automates the cleanup of merge requests in GitLab by checking their associated Jira tickets and handling merge conflicts. This tool helps maintain clean repositories by automatically managing stale merge requests.

## Features

- 🔍 Automatically scans specified GitLab repositories for open merge requests
- 🎫 Integrates with Jira to check ticket status
- 🔄 Automatically closes MRs associated with closed Jira tickets
- ⚠️ Detects and notifies authors about merge conflicts
- 📝 Adds informative comments to MRs before closing
- 📊 Logs all actions for review
- 👥 Supports filtering MRs by specific authors

## Prerequisites

- Python 3.x
- GitLab API access token
- Jira API access token
- Required Python packages (see `requirements.txt`)

## Configuration

1. Create a `config.py` file in the root directory with the following structure:

```python
GITLAB_API_URL = "https://gitlab.com/api/v4"
GIT_HEADERS = {
    "PRIVATE-TOKEN": "your_gitlab_token"
}

JIRA_API_URL = "https://your-domain.atlassian.net/rest/api/3"
JIRA_HEADERS = {
    "Authorization": "Basic your_jira_token",
    "Content-Type": "application/json"
}
```

2. Update the target authors list in `clean_up_mrs.py`:
```python
TARGET_AUTHORS = ["john.doe", "jane.smith", "dev.user"]
```

3. Configure the repositories to monitor:
```python
repository_names = [
    "example_org/project_a",
    "example_org/project_b"
]
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Configure your GitLab and Jira credentials in `config.py`
2. Update the target authors and repositories in `clean_up_mrs.py`
3. Run the script:
```bash
python clean_up_mrs.py
```

## How It Works

1. The script fetches all open merge requests from the specified repositories
2. For each MR:
   - Checks if the author is in the target list
   - Extracts the associated Jira ticket key from the MR title/description
   - Verifies the Jira ticket status
   - If the Jira ticket is closed:
     - Adds a comment explaining the closure
     - Closes the merge request
   - If the Jira ticket is open:
     - Checks for merge conflicts
     - If conflicts exist, notifies the author
     - If no conflicts, logs the status

## Logging

The script maintains detailed logs of all actions performed, including:
- Number of MRs found in each repository
- Actions taken on each MR
- Any errors or issues encountered
- Comments added to MRs
- MR closures

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the repository or contact the maintainers.

## ☕ Support My Work

If this tool saved you time or effort, consider buying me a coffee.  
Your support helps me keep building and maintaining open-source projects like this!

You can either scan the QR code below or click the link to tip me:

👉 [**buymeacoffee.com/ashfaqueali**](https://buymeacoffee.com/ashfaqueali)

<img src="https://ashfaqsolangi.com/images/bmc_qr.png" alt="Buy Me a Coffee QR" width="220" height="220" />
