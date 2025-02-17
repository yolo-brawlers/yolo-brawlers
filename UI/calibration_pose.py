from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QDialog, QSpacerItem, QSizePolicy, QDesktopWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class CalibrationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calibrate Position")
        screen_geometry = QDesktopWidget().availableGeometry()
        x_pos = (screen_geometry.width() - 1000) // 2
        y_pos = (screen_geometry.height() - 800) // 2
        self.setGeometry(x_pos, y_pos, 1000, 800)  # Increased the window size
        # Layout for the dialog
        layout = QVBoxLayout(self)

        # Instruction label
        label = QLabel(
            "The camera will open on your screen and the screen will be divided into 3 zone.\n "
            "You can:\n"
            "0. Guard (Stay in the middle zone with your arms in a guard position)\n"
            "1. Punch right (extend your left arm to the right zone)\n"
            "2. Punch left (extend you right arm to the left zone)\n"
            "3. Weave right (move your face to the right zone)\n"
            "4. Weave left (move your face to the left zone)\n"
            "Your actions will control the robot!\n"
            "Click 'Continue' when you are ready.",
            self,
        )
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(label)

        # Spacer for better separation between text and image
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addSpacerItem(spacer)

        # Image placeholder
        image_label = QLabel(self)
        pixmap = QPixmap("assets/yolo.png")  # Load the image
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                800, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(image_label)

        # Spacer for better separation between image and button
        layout.addSpacerItem(spacer)

        # "Continue" button
        continue_button = QPushButton("Continue", self)
        continue_button.clicked.connect(self.accept)  # Closes the dialog
        continue_button.setStyleSheet(
            "font-size: 16px; padding: 10px 20px;"  # Larger font and padding
        )
        layout.addWidget(continue_button, alignment=Qt.AlignCenter)
