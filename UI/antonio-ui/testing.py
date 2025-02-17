from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QDesktopWidget
from PyQt5.QtGui import QPixmap, QFontDatabase, QFont
from PyQt5.QtCore import Qt, QTimer
import sys


class PixelArtViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yolo Brawlers")

        # Main container (stacked widget)
        self.main_widget = QStackedWidget(self)

        # Get screen size
        screen_geometry = QDesktopWidget().availableGeometry()
        window_width = 1500
        window_height = 1000

        # Calculate the position to center the window
        x_pos = (screen_geometry.width() - window_width) // 2
        y_pos = (screen_geometry.height() - window_height) // 2

        # Set the window geometry to center the window on the screen
        self.setGeometry(x_pos, y_pos, window_width, window_height)

        # Page 1: Pixel art background with text
        page1 = QWidget(self)
        self.page1_layout = QVBoxLayout(page1)

        # Pixel art background label (to set as the background image)
        label = QLabel(self)
        pixmap = QPixmap("space_background.png")

        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                window_width, window_height, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            label.setPixmap(scaled_pixmap)
        label.setScaledContents(True)
        # Make sure it fills the entire window
        label.setGeometry(0, 0, window_width, window_height)

        # Title label
        pixel_font_id = QFontDatabase.addApplicationFont("VT323-Regular.ttf")
        pixel_font_family = QFontDatabase.applicationFontFamilies(
            pixel_font_id)
        if pixel_font_family:
            pixelated_font = QFont(pixel_font_family[0], 24)
        else:
            pixelated_font = QFont("Arial", 24)  # Fallback font

        title_font_id = QFontDatabase.addApplicationFont("karma-future.otf")
        title_font_family = QFontDatabase.applicationFontFamilies(
            title_font_id)
        if title_font_family:
            title_font = QFont(title_font_family[0], 50)
        else:
            title_font = QFont("Arial", 50)  # Fallback font

        # Add "YOLO BRAWLERS" title
        self.title_label = QLabel("YOLO BRAWLERS", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet(
            "color: white; background-color: rgba(0, 0, 0, 0);")
        self.title_label.setGeometry(
            window_width // 2 - 600, 200, 1200, 200)  # Position it over the image

        # "Click to Start" label
        self.click_to_start_label = QLabel("Click to Start", self)
        self.click_to_start_label.setAlignment(Qt.AlignCenter)
        self.click_to_start_label.setFont(pixelated_font)
        self.click_to_start_label.setStyleSheet(
            "color: white; background-color: rgba(0, 0, 0, 0);")
        self.click_to_start_label.setGeometry(
            window_width // 2 - 400, window_height // 2, 800, 200)  # Position it over the image

        # Set the first page
        self.main_widget.addWidget(page1)

        # Set stacked widget as the central widget
        self.setCentralWidget(self.main_widget)

        # Set up a timer for the flashing effect on the "Click to Start" label
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.toggle_visibility)
        self.timer.start(1000)

    def toggle_visibility(self):
        self.click_to_start_label.setVisible(
            not self.click_to_start_label.isVisible())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = PixelArtViewer()
    viewer.show()
    sys.exit(app.exec_())
