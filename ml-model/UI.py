import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys
import os
from yolo_fightingpose_detection import ZonePoseDetector  # Import YOLO detector

# VideoThread used to display computer vision camera
class VideoThread(QThread):
    update_frame = pyqtSignal(np.ndarray)


    def __init__(self, cpuType):
        super().__init__()
        self.detector = ZonePoseDetector()
        self.cap = cv2.VideoCapture(cpuType)
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)  # Flip frame horizontally for a mirror effect
                annotated_frame, pose = self.detector.process_frame(frame)
                
                # Print the detected pose in the terminal
                if pose:
                    print(f"Detected Pose: {pose.value}")
                
                # Sends signal to update_frame
                self.update_frame.emit(annotated_frame)

    def stop(self):
        self.running = False
        self.cap.release()
        self.quit()
        self.wait()


# Main Window to start or stop camera
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fighting Pose Detection")
        self.setGeometry(100, 100, 800, 600)

        # Title Label in a Bigger Textbox
        self.title_box = QLabel(self)  # Create a box to hold the label
        self.title_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_box.setStyleSheet("border: 2px solid black; background-color: white; padding: 10px;")  # Border & BG color
        self.title_box.setFixedSize(400, 100)  # Increase textbox size

        # Inside the box, place the actual label
        self.title_label = QLabel("Welcome to YOLO Brawlers", self.title_box)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))  # Bigger Font
        self.title_label.setWordWrap(True)  # Allow text wrapping
        self.title_label.setGeometry(10, 10, 380, 80)  # Adjust label within the box



        # Video Display (for OpenCV camera)
        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("border: 2px solid black;")  # Optional: Add a border

        # Set Maximum Size to Prevent Overlapping Buttons
        self.video_label.setMaximumSize(800, 450)  # Adjust dimensions as needed
        self.video_label.setScaledContents(True)  # Ensure the video scales properly


        self.start_button = QPushButton("Start Camera", self)
        self.start_button.clicked.connect(self.start_video)

        self.stop_button = QPushButton("Stop Camera", self)
        self.stop_button.clicked.connect(self.stop_video)
        self.stop_button.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

        self.thread = None

    def start_video(self):
        self.title_label.hide()  # Hide the title label when starting the camera
        self.video_label.setStyleSheet("border: 2px solid black;")  # Add black border
        self.thread = VideoThread(int(sys.argv[1]))
        self.thread.update_frame.connect(self.display_video_frame)
        self.thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_video(self):
        if self.thread:
            self.thread.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.title_label.show()  # Show title label when stopping the camera
        self.video_label.setStyleSheet("border: none;")  # Remove the black border

    def display_video_frame(self, frame):
        """Convert OpenCV frame to PyQt QImage and display in QLabel."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_frame.shape
        bytes_per_line = 3 * width
        qt_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
