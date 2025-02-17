# GitLab Cloner

## The Struggle

When I started working with GitLab on a large-scale project, I encountered a huge inconvenience. Whenever I needed to make changes, I would need to clone each project one by one, especially if the project had many nested groups, subgroups, and repositories. GitLab does not provide an easy way to clone the entire structure in one go, leaving me with a tedious and time-consuming process.

This led me to build a solution: **GitLab Cloner**. This application automatically clones all the projects in a given group, subgroup, and even sub-subgroups while maintaining the exact folder structure. It's a time-saver that significantly improves the workflow, especially when dealing with large projects.

## Features

- **Automatic Cloning**: Clone all repositories from a GitLab group, including subgroups and sub-subgroups.
- **Maintains Structure**: The folder structure is preserved as per the GitLab group hierarchy.
- **Real-time Progress**: Monitor the cloning progress with a built-in progress bar and logs.
- **Theme Switch**: Toggle between light and dark themes for a customized experience.

## Screenshots

![App Screenshot](assets\blackmode.png)
![App Screenshot](assets\lightmode.png)

> **Note**: A screenshot of the app interface can be added once the application is running.

## Installation

Follow the steps below to get the application up and running on your local machine.

### Requirements

- **Python** version 3.x or higher
- **PyQt5** for the GUI
- **requests** for API calls to GitLab
- **python-dotenv** for environment variable management
- **Git** for cloning repositories

You can install the necessary dependencies by running:

```bash
pip install -r requirements.txt
```

## Clone the Repository

```bash
git clone https://github.com/mhazem-bouaziz/gitlab-cloner.git
cd gitlab-cloner
```

## How It Works

The application connects to your GitLab account via the GitLab API and retrieves all groups and subgroups. Once it has this structure, it clones all the projects into your local machine while maintaining the same folder hierarchy.

- Step 1: Enter your GitLab token, group ID, and desired local path.
- Step 2: Click Start Cloning to begin the cloning process.
- Step 3: Monitor the progress and log output as each project is cloned.
- Step 4: Once the cloning is complete, a success message will notify you.

## Usage

After setting up the environment, run the application with the following command:

```bash
python main_window.py
```

Then, use the GUI to enter the required details (GitLab token, group ID, base path) and click Start Cloning.

## Contributing

Contributions are welcome! If you encounter bugs or want to enhance the functionality, feel free to fork the repository and open a pull request.

- Fork the repo
- Create a new branch for your feature (`git checkout -b feature-name`)
- Make your changes
- Commit your changes (`git commit -am 'Add feature'`)
- Push to the branch (`git push origin feature-name`)
- Create a new pull request

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.