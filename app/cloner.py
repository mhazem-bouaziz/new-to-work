import os
import subprocess
import requests
import logging

# Logging configuration
logging.basicConfig(
    filename="gitlab_cloner.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def get_projects_in_group(group_id, token):
    GITLAB_URL = 'https://gitlab.admiral-eu.com'  # Your GitLab instance URL
    headers = {'Private-Token': token}
    try:
        response = requests.get(f"{GITLAB_URL}/api/v4/groups/{group_id}/projects?per_page=100", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching projects for group {group_id}: {e}")
        return []

def fetch_all_projects_thread(group_id, token, base_path, progress_callback, log_callback):
    projects = get_projects_in_group(group_id, token)

    # Clone projects in the current group/subgroup
    if projects:
        clone_projects_thread(projects, base_path, progress_callback, log_callback)

    # Fetch and recurse into subgroups
    subgroups = get_subgroups(group_id, token)
    for subgroup in subgroups:
        subgroup_name = subgroup['name']
        subgroup_id = subgroup['id']
        subgroup_path = os.path.join(base_path, subgroup_name)
        os.makedirs(subgroup_path, exist_ok=True)  # Create directory for the subgroup
        fetch_all_projects_thread(subgroup_id, token, subgroup_path, progress_callback, log_callback)

def get_subgroups(group_id, token):
    GITLAB_URL = 'https://gitlab.admiral-eu.com'  # Your GitLab instance URL
    headers = {'Private-Token': token}
    try:
        response = requests.get(f"{GITLAB_URL}/api/v4/groups/{group_id}/subgroups?per_page=100", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching subgroups for group {group_id}: {e}")
        return []

def clone_projects_thread(projects, parent_path, progress_callback, log_callback):
    total_projects = len(projects)
    for i, project in enumerate(projects):
        repo_url = project['ssh_url_to_repo']
        project_name = project['name']
        project_path = os.path.join(parent_path, project_name)

        os.makedirs(project_path, exist_ok=True)  # Ensure directory exists

        log_callback(f"Cloning {repo_url}...")
        try:
            result = subprocess.run(['git', 'clone', repo_url, project_path], capture_output=True, text=True)
            if result.returncode == 0:
                log_callback(f"Successfully cloned {repo_url}")
            else:
                log_callback(f"Failed to clone {repo_url}: {result.stderr}")
        except subprocess.CalledProcessError as e:
            log_callback(f"Error during cloning project {repo_url}: {e}")
        except Exception as e:
            log_callback(f"Unexpected error while cloning project {repo_url}: {e}")
        
        progress_callback(int((i + 1) / total_projects * 100))
