import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLineEdit, QProgressBar, QTextEdit, QMessageBox, QStatusBar, QWidget, QToolTip
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QPropertyAnimation, QRect
from PyQt5.QtGui import QColor, QIcon, QPainter, QPixmap
from cloner import fetch_all_projects_thread
from utils import validate_token


class ClonerWorker(QThread):
    progress_signal = pyqtSignal(int)
    log_signal = pyqtSignal(str)
    complete_signal = pyqtSignal()

    def __init__(self, group_id, token, base_path):
        super().__init__()
        self.group_id = group_id
        self.token = token
        self.base_path = base_path

    def run(self):
        fetch_all_projects_thread(self.group_id, self.token, self.base_path, self.update_progress, self.update_log)
        self.complete_signal.emit()  # Emit when cloning is finished

    def update_progress(self, progress):
        self.progress_signal.emit(progress)

    def update_log(self, message):
        self.log_signal.emit(message)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GitLab Cloner")
        self.setGeometry(100, 100, 600, 500)
        self.setWindowIcon(QIcon("gitlab_icon.png"))

        self.current_theme = 'light'  # Default theme is light

        layout = QVBoxLayout()

        # Input fields
        self.group_id_input = QLineEdit(self)
        self.group_id_input.setPlaceholderText("Enter Group ID")
        self.group_id_input.setToolTip("Enter the GitLab group ID from which to clone projects.")

        self.token_input = QLineEdit(self)
        self.token_input.setPlaceholderText("Enter GitLab Token")
        self.token_input.setToolTip("Enter your GitLab personal access token.")
        self.token_input.setEchoMode(QLineEdit.Password)

        self.base_path_input = QLineEdit(self)
        self.base_path_input.setPlaceholderText("Enter Base Path")
        self.base_path_input.setToolTip("Enter the directory path where cloned projects will be saved.")

        # Buttons
        self.start_button = QPushButton("Start Cloning", self)
        self.start_button.setIcon(QIcon("start_icon.png"))
        self.start_button.clicked.connect(self.start_cloning)

        self.cancel_button = QPushButton("Cancel Cloning", self)
        self.cancel_button.setIcon(QIcon("cancel_icon.png"))
        self.cancel_button.clicked.connect(self.cancel_cloning)
        self.cancel_button.setEnabled(False)

        # Progress Bar
        self.progress_bar = QProgressBar(self)

        # Log Output
        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)

        # Status Bar for extra information
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # Theme Switch Button
        self.switch_theme_button = QPushButton("Switch to Dark Mode", self)
        self.switch_theme_button.clicked.connect(self.toggle_theme)

        # Add widgets to layout
        layout.addWidget(self.group_id_input)
        layout.addWidget(self.token_input)
        layout.addWidget(self.base_path_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.cancel_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.log_output)
        layout.addWidget(self.switch_theme_button)

        # Set the main widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.cloner_thread = None

        # Apply styles
        self.set_styles()

        # Remember last token and group ID for convenience
        self.load_user_preferences()

    def set_styles(self):
        """Method to set up the UI styles using QSS (Qt Style Sheets)"""
        if self.current_theme == 'light':
            self.setStyleSheet("""
                QWidget {
                    background-color: #f8f9fa;
                    font-family: 'Arial', sans-serif;
                }
                QLineEdit {
                    border: 2px solid #ccc;
                    padding: 8px;
                    border-radius: 5px;
                    margin: 5px 0;
                }
                QPushButton {
                    background-color: #007bff;
                    color: white;
                    padding: 10px 15px;
                    border-radius: 5px;
                    font-size: 14px;
                    margin: 10px 0;
                }
                QProgressBar {
                    border: 2px solid #ccc;
                    border-radius: 5px;
                    background-color: #e9ecef;
                    height: 20px;
                    margin-top: 20px;
                }
                QTextEdit {
                    background-color: #ffffff;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    padding: 8px;
                }
                QLabel {
                    font-weight: bold;
                    font-size: 16px;
                }
            """)
            self.switch_theme_button.setText("Switch to Dark Mode")
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #333333;
                    font-family: 'Arial', sans-serif;
                    color: #f1f1f1;
                }
                QLineEdit {
                    border: 2px solid #555;
                    padding: 8px;
                    border-radius: 5px;
                    margin: 5px 0;
                    background-color: #444;
                    color: #f1f1f1;
                }
                QPushButton {
                    background-color: #007bff;
                    color: white;
                    padding: 10px 15px;
                    border-radius: 5px;
                    font-size: 14px;
                    margin: 10px 0;
                }
                QProgressBar {
                    border: 2px solid #555;
                    border-radius: 5px;
                    background-color: #444;
                    height: 20px;
                    margin-top: 20px;
                }
                QTextEdit {
                    background-color: #555;
                    border: 1px solid #777;
                    border-radius: 5px;
                    padding: 8px;
                    color: #f1f1f1;
                }
                QLabel {
                    font-weight: bold;
                    font-size: 16px;
                    color: #f1f1f1;
                }
            """)
            self.switch_theme_button.setText("Switch to Light Mode")

    def toggle_theme(self):
        """Toggle between light and dark modes"""
        if self.current_theme == 'light':
            self.current_theme = 'dark'
        else:
            self.current_theme = 'light'

        self.set_styles()
        self.animate_theme_change()

    def animate_theme_change(self):
        """Smoothly transition between light and dark themes"""
        animation = QPropertyAnimation(self, b"windowOpacity")
        animation.setDuration(500)
        animation.setStartValue(1)
        animation.setEndValue(0)
        animation.finished.connect(self.on_animation_finished)
        animation.start()

    def on_animation_finished(self):
        """Apply changes after the animation is finished"""
        self.set_styles()
        animation = QPropertyAnimation(self, b"windowOpacity")
        animation.setDuration(500)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.start()

    def start_cloning(self):
        # Get user input
        group_id = self.group_id_input.text().strip()
        token = self.token_input.text().strip()
        base_path = self.base_path_input.text().strip()

        # Validate input
        if not group_id or not token or not base_path:
            self.show_error_message("Please fill in all fields.")
            return

        # Validate GitLab token
        if not validate_token(token):
            self.show_error_message("Invalid GitLab token.")
            return

        # Disable the start button and enable cancel
        self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(True)

        # Create and start the worker thread
        self.cloner_thread = ClonerWorker(group_id, token, base_path)
        self.cloner_thread.progress_signal.connect(self.update_progress)
        self.cloner_thread.log_signal.connect(self.append_log)
        self.cloner_thread.complete_signal.connect(self.on_cloning_complete)

        # Start the thread
        self.cloner_thread.start()

        # Update status bar
        self.status_bar.showMessage(f"Cloning in progress...")

    def cancel_cloning(self):
        if self.cloner_thread.isRunning():
            self.cloner_thread.terminate()
        self.cancel_button.setEnabled(False)
        self.start_button.setEnabled(True)

        # Update status bar
        self.status_bar.showMessage("Cloning canceled.")

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def append_log(self, message):
        self.log_output.append(message)

    def on_cloning_complete(self):
        self.progress_bar.setValue(100)
        self.show_info_message("Cloning complete!")
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(False)

        # Reset progress bar
        self.progress_bar.reset()

        # Update status bar
        self.status_bar.showMessage("Cloning completed successfully.")

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec_()

    def show_info_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Success")
        msg.setText(message)
        msg.exec_()

    def load_user_preferences(self):
        """Load user preferences like last token and group ID"""
        # Here, you could save preferences and load them upon starting the app
        # Example: Load last used group ID, token, and base path
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
