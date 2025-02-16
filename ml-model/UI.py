import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys
import os
from yolo_fightingpose_detection import ZonePoseDetector
from controller import ToyController
from client import handle_pose

class VideoThread(QThread):
    """
    A separate thread for handling real-time video capture and processing.

    This class:
    - Captures video frames from the OpenCV camera.
    - Processes frames using YOLO pose detection.
    - Emits processed frames to update the UI without freezing it.

    Attributes:
        update_frame (pyqtSignal): Signal to send processed frames to the main UI.
        detector (ZonePoseDetector): YOLO-based pose detection model.
        cap (cv2.VideoCapture): OpenCV camera object.
        running (bool): Flag to control the video thread.
    """

    update_frame = pyqtSignal(np.ndarray)

    def __init__(self, cpuType):
        """
        Initializes the video thread.

        Args:
            cpuType (int): The index of the camera device.
        """
        super().__init__()
        self.detector = ZonePoseDetector()
        self.controller = ToyController()
        self.cap = cv2.VideoCapture(cpuType)

        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            self.stop()
        else:
            self.running = True
            # Connect to the ESP32
            if not self.ontroller.connect():
                print("Failed to connect to ESP32.")
                self.stop()

    def run(self):
        """
        Runs the video processing loop.

        - Reads frames from OpenCV.
        - Processes them using YOLO pose detection.
        - Emits the processed frame to update the UI.
        - Calls `handle_pose` when a new pose is detected.
        """
        current_pose = None
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)  # Flip frame horizontally for a mirror effect
                annotated_frame, pose = self.detector.process_frame(frame)

                # Act on new pose detection
                if pose and pose != current_pose:
                    print(f"Detected Pose: {pose.value}")
                    current_pose = pose
                    handle_pose(pose, self.controller)

                # Display the annotated frame
                cv2.imshow("Fighting Pose Detection", annotated_frame)

                # Emit the frame to update the UI
                self.update_frame.emit(annotated_frame)
            else:
                print("Error: Failed to capture frame!")

    def stop(self):
        """
        Stops the video processing thread.

        - Releases the OpenCV camera.
        - Closes any OpenCV windows.
        - Stops the running thread.
        """
        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()
        self.controller.close()
        self.quit()
        self.wait()


class MainWindow(QWidget):
    """
    The main UI window for the Fighting Pose Detection application.

    This class:
    - Displays a title box before the camera starts.
    - Shows a live video feed from OpenCV.
    - Provides "Start Camera" and "Stop Camera" buttons to control video capture.

    Attributes:
        title_box (QLabel): Container for the title text.
        title_label (QLabel): Displays "Welcome to YOLO Brawlers".
        video_label (QLabel): Displays video frames.
        start_button (QPushButton): Starts the camera feed.
        stop_button (QPushButton): Stops the camera feed.
        thread (VideoThread): The separate video processing thread.
    """

    def __init__(self):
        """
        Initializes the main window and its UI components.
        """
        super().__init__()

        self.setWindowTitle("Fighting Pose Detection")
        self.setGeometry(100, 100, 800, 600)

        # Title Label in a Bigger Textbox
        self.title_box = QLabel(self)  # Create a box to hold the label
        self.title_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_box.setStyleSheet("border: 2px solid black; background-color: white; padding: 10px;")
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
        self.video_label.setStyleSheet("border: 2px solid black;")

        # Set Maximum Size to Prevent Overlapping Buttons
        self.video_label.setMaximumSize(800, 450)  # Adjust dimensions as needed
        self.video_label.setScaledContents(True)  # Ensure the video scales properly

        # Buttons
        self.start_button = QPushButton("Start Camera", self)
        self.start_button.clicked.connect(self.start_video)

        self.stop_button = QPushButton("Stop Camera", self)
        self.stop_button.clicked.connect(self.stop_video)
        self.stop_button.setEnabled(False)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

        self.thread = None

    def start_video(self):
        """
        Starts the video feed by initializing a VideoThread instance.

        - Hides the title label when the camera starts.
        - Applies a black border to the video label.
        - Disables the start button and enables the stop button.
        - Begins the video processing thread.
        """
        self.title_label.hide()
        self.video_label.setStyleSheet("border: 2px solid black;")
        self.thread = VideoThread(int(sys.argv[1]))
        self.thread.update_frame.connect(self.display_video_frame)
        self.thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_video(self):
        """
        Stops the video feed and resets UI elements.

        - Stops the video processing thread if running.
        - Enables the start button and disables the stop button.
        - Shows the title label when stopping the camera.
        - Removes the black border from the video label.
        """
        if self.thread:
            self.thread.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.title_label.show()
        self.video_label.setStyleSheet("border: none;")

    def display_video_frame(self, frame):
        """
        Converts an OpenCV frame to a QImage and displays it in the UI.

        Args:
            frame (numpy.ndarray): The processed frame from OpenCV.
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_frame.shape
        bytes_per_line = 3 * width
        qt_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))


if __name__ == "__main__":
    """
    Entry point for the PyQt5 application.

    - Creates an instance of `MainWindow`.
    - Starts the Qt event loop.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
