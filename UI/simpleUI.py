import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

sys.path.append('../')

from client.PoseController import PoseController


class MainWindow(QWidget):
    """
    Main UI window with two options:
    1. Open the OpenCV camera
    2. Use the keyboard controller
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select Mode")
        self.setGeometry(100, 100, 800, 600)

        # Layout
        layout = QVBoxLayout()

        # Title Label
        title = QLabel("Welcome to the Application", self)
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Buttons
        btn_camera = QPushButton("Open OpenCV Camera", self)
        btn_camera.clicked.connect(self.open_camera)

        # btn_keyboard = QPushButton("Use Keyboard Controller", self)
        # btn_keyboard.clicked.connect(self.start_keyboard_controller)

        # Add widgets to layout
        layout.addWidget(title)
        layout.addWidget(btn_camera)
        # layout.addWidget(btn_keyboard)
        layout.addStretch()

        self.setLayout(layout)

    def open_camera(self):
        """Opens the OpenCV camera directly in a new window."""
        controller = PoseController()
        if controller.connect():
            controller.run_yolo_mode()
        else:
            print("Failed to connect to ESP32.")

    def start_keyboard_controller(self):
        """Starts the keyboard controller from the client module."""
        # self.controller = KeyboardController()  # Replace with actual class
        self.controller.run()  # Start the keyboard controller

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
