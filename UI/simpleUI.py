import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QRadioButton, QPushButton, QButtonGroup, QGroupBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import os

sys.path.append('../')

from client.PoseController import PoseController
# from client.KeyboardController import KeyboardController

ESP32_MAP = {
    0: "192.168.4.2",
    1: "192.168.4.4"
}

CAMERA_MAP = {
    0: "Intel/AMD",
    1: "Apple Silicon"
}

class MainWindow(QWidget):
    """
    Main UI window with two options:
    1. Open the OpenCV camera
    2. Use the keyboard controller
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("YOLO Brawlers")
        self.setGeometry(100, 100, 800, 600)

        # Layout
        self.main_layout = QVBoxLayout()

        # self.Title Label
        self.title = QLabel("Welcome to YOLO Brawlers", self)
        self.title.setFont(QFont("Roboto", 28, QFont.Weight.Bold))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Robot ID Section
        self.robot_id_group = QGroupBox("Robot ID")
        self.robot_id_group.setFont(QFont("Roboto", 20, QFont.Weight.ExtraBold))
        self.robot_id_layout = QVBoxLayout()

        # Buttons
        self.btn_camera = QPushButton("Open OpenCV Camera", self)
        self.btn_camera.clicked.connect(self.open_camera)

        # Radio Button Group for toy_id Selection
        self.radio_toy_group = QButtonGroup(self)
        self.radio_toy_0 = QRadioButton("0")
        self.radio_toy_1 = QRadioButton("1")
        self.radio_toy_0.setChecked(True)  # Default selection(Robot ID 0 is selcted)
        self.radio_toy_group.addButton(self.radio_toy_0, 0)
        self.radio_toy_group.addButton(self.radio_toy_1, 1)

        # Add radio buttons to Robot ID layout
        self.robot_id_layout.addWidget(self.radio_toy_0)
        self.robot_id_layout.addWidget(self.radio_toy_1)

        # Add robot id layout to robot id group box
        self.robot_id_group.setLayout(self.robot_id_layout)

        self.test_connection_layout = QVBoxLayout()
        self.test_connection_group = QGroupBox("Connection Test")
        self.test_connection_group.setFont(QFont("Roboto", 20, QFont.Weight.ExtraBold))

        # Test connection button of robot section
        self.btn_test_connection = QPushButton("Test Connection on Robot")
        self.btn_test_connection.clicked.connect(self.test_robot_connection)

        # Test connection status label
        self.connection_status = QLabel("", self)
        self.connection_status.setFont(QFont("Roboto", 14, QFont.Weight.Bold))

        self.test_connection_layout.addWidget(self.btn_test_connection)
        self.test_connection_layout.addWidget(self.connection_status)
        self.test_connection_group.setLayout(self.test_connection_layout)

        # Choose Chip Type for CV Camera
        self.chip_group = QGroupBox("Chip Type for CV Camera")
        self.chip_group.setFont(QFont("Roboto", 20, QFont.Weight.ExtraBold))
        self.chip_layout = QVBoxLayout()

        # Radio Button Group for toy_id Selection
        self.radio_chip_group = QButtonGroup(self)
        self.radio_chip_0 = QRadioButton("Intel/AMD")
        self.radio_chip_1 = QRadioButton("Apple Silicon")
        self.radio_chip_0.setChecked(True)  # Default selection(Intel/AMD is selected)
        self.radio_chip_group.addButton(self.radio_chip_0, 0)
        self.radio_chip_group.addButton(self.radio_chip_1, 1)

        self.chip_layout.addWidget(self.radio_chip_0)
        self.chip_layout.addWidget(self.radio_chip_1)
        self.chip_group.setLayout(self.chip_layout)

        # Add widgets to layout
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.robot_id_group)
        self.main_layout.addWidget(self.test_connection_group)
        self.main_layout.addWidget(self.chip_group)
        self.main_layout.addWidget(self.btn_camera)
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)

    def open_camera(self):
        """Opens the OpenCV camera directly in a new window."""
        selected_robot_id = self.radio_toy_group.checkedId()  # Get selected radio button value
        camera_mode = self.radio_chip_group.checkedId()
        print(camera_mode)
        print(f"Selected Robot ID: {selected_robot_id}")  # Print robot id to console
        controller = PoseController(toy_id=selected_robot_id)
        if controller.connect():
            controller.run_yolo_mode(camera_mode)
        else:
            print("Failed to connect to ESP32.")

    def start_keyboard_controller(self):
        """Starts the keyboard controller from the client module."""
        # self.controller = KeyboardController()  # Replace with actual class
        # self.controller.run()  # Start the keyboard controller
        pass
    
    def test_robot_connection(self):
        """Pings the detected local IP address and updates the UI with success/failure."""
        try:
            ip_address = os.popen("ipconfig getifaddr en0").read().strip()  # Get IP address
            print(ip_address)
            if not ip_address:
                self.connection_status.setText("❌ Error: Could not retrieve IP address.")
                self.connection_status.setStyleSheet("color: red;")  # Red for error
                return

            selected_robot_id = self.radio_toy_group.checkedId()  # Get selected radio button value
            print(f"Pinging Robot {selected_robot_id}...")  # Print robot id

            response = os.system(f"ping -c 2 {ESP32_MAP[int(selected_robot_id)]} > /dev/null 2>&1")  # Run ping command

            if response == 0:
                self.connection_status.setText(f"✅ Connection Successful to Robot {selected_robot_id}!")
                self.connection_status.setStyleSheet("color: green;")  # Green for success
            else:
                self.connection_status.setText(f"❌ Connection Failed to Robot {selected_robot_id}!")
                self.connection_status.setStyleSheet("color: red;")  # Red for failure
        
        except Exception as e:
            self.connection_status.setText(f"❌ Error: {e}")
            self.connection_status.setStyleSheet("color: red;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
