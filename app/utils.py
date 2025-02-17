import requests

def validate_token(token):
    GITLAB_URL = "https://gitlab.admiral-eu.com"  # Your GitLab instance URL
    headers = {"Private-Token": token}
    try:
        response = requests.get(f"{GITLAB_URL}/api/v4/user", headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return True
    except requests.exceptions.RequestException as e:
        return False
