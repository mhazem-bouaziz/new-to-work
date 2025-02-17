# How to Set Up and Run the GitLab Cloner

This document provides instructions for setting up and running the **GitLab Cloner** application on your local machine.

## Prerequisites

1. **Install Python 3.x**: This application is built using Python, so you need Python 3.x or higher installed. You can download Python from the official site: [Python Downloads](https://www.python.org/downloads/).
   
2. **Install Git**: Git must be installed to clone the repositories. You can download it from: [Git Downloads](https://git-scm.com/downloads).

3. **Create a GitLab Personal Access Token**:
   - Go to [GitLab](https://gitlab.com) and log in to your account.
   - Navigate to `User Settings` > `Access Tokens`.
   - Create a token with `api` scope and save it, as you will need it to authenticate with the GitLab API.

4. **Clone the Repository**:
   - Open a terminal or command prompt.
   - Run the following command to clone the GitLab Cloner repository:
   
   ```bash
   git clone https://github.com/mhazem-bouaziz/gitlab-cloner.git
   cd gitlab-cloner
   ```

## Setting Up the Environment

### Step 1: Install Python Dependencies

Once the repository is cloned, you need to install the required Python packages.

1- Navigate to the cloned directory if you're not already there.
2- Install the dependencies using pip:

```bash
pip install -r requirements.txt
```

### Step 2: Set Up Environment Variables

Create a .env file in the root directory of the project to store sensitive information like your GitLab token and other configuration settings.

The .env file should look like this:

```dotenv
GITLAB_URL=https://gitlab.com  # Your GitLab URL
GITLAB_TOKEN=your_personal_access_token  # Your GitLab token
DEFAULT_BASE_PATH=C:/path/to/clone  # Base path for saving cloned repositories
```

Replace the values with your actual GitLab token and desired local path.

### Step 3: Run the Application

1- After setting up the environment, you can run the application by executing the following command:

```bash
python main_window.py
```

2- The app will open, and you will be prompted to enter:

    - Group ID: The ID of the GitLab group you want to clone.
    - GitLab Token: Your personal access token for authentication.
    - Base Path: The directory path where cloned repositories will be saved.

3- Once you have entered the necessary information, click Start Cloning to begin the cloning process.

## Troubleshooting

- If the app doesn't start, ensure that Python is correctly installed and the dependencies are up to date.

- If you encounter any issues with cloning or authentication, double-check your GitLab token and the entered group ID.