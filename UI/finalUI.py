from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                            QGroupBox, QRadioButton, QButtonGroup, QStackedWidget,
                            QFrame, QSizePolicy, QApplication, QDesktopWidget)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor, QPalette, QFontDatabase
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
import sys

sys.path.append("../")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("YOLO Brawlers")
        
        # Get screen size
        screen_geometry = QDesktopWidget().availableGeometry()
        self.window_width = 1200
        self.window_height = 800

        # Calculate the position to center the window
        x_pos = (screen_geometry.width() - self.window_width) // 2
        y_pos = (screen_geometry.height() - self.window_height) // 2

        # Set the window geometry to center the window on the screen
        self.setGeometry(x_pos, y_pos, self.window_width, self.window_height)
        
        # Create stacked widget for multiple pages
        self.stacked_widget = QStackedWidget()
        
        # Load fonts
        self.load_fonts()

        # Store selected player
        self.selected_player = None
        
        # Create pages
        self.create_pixel_art_start_page()
        self.create_player_selection_page()
        
        # Set central widget
        # self.setCentralWidget(self.stacked_widget)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)
        
        # Set initial page
        self.stacked_widget.setCurrentIndex(0)
        
        

    def load_fonts(self):
        """Load custom fonts for pixel art style"""
        # Pixel font for regular text
        self.pixel_font_id = QFontDatabase.addApplicationFont("VT323-Regular.ttf")
        self.pixel_font_family = QFontDatabase.applicationFontFamilies(self.pixel_font_id)
        if self.pixel_font_family:
            self.pixelated_font = QFont(self.pixel_font_family[0], 24)
        else:
            self.pixelated_font = QFont("Arial", 24)  # Fallback font

        # Title font for main headings
        self.title_font_id = QFontDatabase.addApplicationFont("karma-future.otf")
        self.title_font_family = QFontDatabase.applicationFontFamilies(self.title_font_id)
        if self.title_font_family:
            self.title_font = QFont(self.title_font_family[0], 50)
        else:
            self.title_font = QFont("Arial", 50)  # Fallback font
    
    def create_pixel_art_start_page(self):
        """Create the start page with pixel art background"""
        start_page = QWidget()
        
        # Pixel art background label
        background_label = QLabel(start_page)
        pixmap = QPixmap("space_background.png")

        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                self.window_width, self.window_height, 
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            background_label.setPixmap(scaled_pixmap)
        background_label.setScaledContents(True)
        # Make sure it fills the entire window
        background_label.setGeometry(0, 0, self.window_width, self.window_height)

        # "YOLO BRAWLERS" title
        self.title_label = QLabel("YOLO BRAWLERS", start_page)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(self.title_font)
        self.title_label.setStyleSheet(
            "color: white; background-color: rgba(0, 0, 0, 0);")
        self.title_label.setGeometry(
            self.window_width // 2 - 600, 200, 1200, 200)

        # "Click to Start" label
        self.click_to_start_label = QLabel("Click to Start", start_page)
        self.click_to_start_label.setAlignment(Qt.AlignCenter)
        self.click_to_start_label.setFont(self.pixelated_font)
        self.click_to_start_label.setStyleSheet(
            "color: white; background-color: rgba(0, 0, 0, 0);")
        self.click_to_start_label.setGeometry(
            self.window_width // 2 - 400, self.window_height // 2, 800, 200)

        # Set up a timer for the flashing effect
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.toggle_visibility)
        self.timer.start(1000)
        
        # Make the start page clickable
        start_page.mousePressEvent = lambda event: self.go_to_player_selection()
        
        self.stacked_widget.addWidget(start_page)
    
    def toggle_visibility(self):
        """Toggle visibility of the 'Click to Start' label"""
        self.click_to_start_label.setVisible(
            not self.click_to_start_label.isVisible())
    
    def create_start_page(self):
        """Create the start page with logo and start button"""
        start_page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Title with large font
        title = QLabel("YOLO Brawlers", start_page)
        title.setFont(QFont("Roboto", 48, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin: 50px;")
        
        # Subtitle
        subtitle = QLabel("Get ready to brawl!", start_page)
        subtitle.setFont(QFont("Roboto", 24))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #7f8c8d; margin-bottom: 100px;")
        
        # Logo placeholder
        logo = QLabel(start_page)
        # Replace this with your actual logo
        # logo.setPixmap(QPixmap("path_to_your_logo.png").scaled(300, 300, Qt.KeepAspectRatio))
        logo.setStyleSheet("background-color: #3498db; border-radius: 150px;")
        logo.setFixedSize(300, 300)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Start button
        start_button = QPushButton("START GAME", start_page)
        start_button.setFont(QFont("Roboto", 20, QFont.Weight.Bold))
        start_button.setMinimumHeight(80)
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #16a085;
            }
        """)
        start_button.clicked.connect(self.go_to_player_selection)
        
        # Add widgets to layout with spacers
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)
        layout.addWidget(start_button)
        layout.addStretch(1)
        
        start_page.setLayout(layout)
        self.stacked_widget.addWidget(start_page)
    
    def create_player_selection_page(self):
        """Create the player selection page with player cards"""
        player_page = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Choose Your Player", player_page)
        title.setFont(QFont("Roboto", 36, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin: 30px;")
        
        # Player selection area
        players_layout = QHBoxLayout()
        players_layout.setSpacing(35)
        players_layout.setContentsMargins(40, 20, 40, 20)
        
        # Player 1 card
        player1_frame = self.create_player_card("Player 1", "player1.png", 0)
        players_layout.addWidget(player1_frame)
        
        # Player 2 card
        player2_frame = self.create_player_card("Player 2", "player2.png", 1)
        players_layout.addWidget(player2_frame)
        
        # Continue button
        continue_button = QPushButton("CONTINUE", player_page)
        continue_button.setFont(QFont("Roboto", 18, QFont.Weight.Bold))
        continue_button.setMinimumHeight(60)
        continue_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
        """)
        continue_button.clicked.connect(self.go_to_control_page)
        
        # Back button
        back_button = QPushButton("Back", player_page)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #7f8c8d;
                border: none;
                padding: 5px;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #2c3e50;
            }
        """)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        
        # Add widgets to layout
        layout.addWidget(title)
        layout.addLayout(players_layout)
        layout.addStretch(1)
        layout.addWidget(continue_button)
        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)
        
        player_page.setLayout(layout)
        self.stacked_widget.addWidget(player_page)
    
    def create_player_card(self, name, image_path, player_id):
        """Create a styled player card with drop shadow"""
        frame = QFrame()
        if name == "Player 1":

            frame.setStyleSheet("""
                QFrame {
                    background-color: #f76c59;
                    border-radius: 15px;
                    padding: 15px;
                }
            """)
        else:
            frame.setStyleSheet("""
                QFrame {
                    background-color: #4382e8;
                    border-radius: 15px;
                    padding: 15px;
                }
            """)

        frame.setFixedSize(320, 400)
        frame.setCursor(Qt.PointingHandCursor)
        
        # Add drop shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(5, 5)
        frame.setGraphicsEffect(shadow)
        
        # Card layout
        card_layout = QVBoxLayout(frame)
        
        # Player image (placeholder)
        image = QLabel()
        try:
            pixmap = QPixmap(image_path)
            image.setPixmap(pixmap.scaled(280, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except:
            image.setStyleSheet("background-color: #2c3e50; border-radius: 10px;")
            image.setFixedSize(280, 280)
        
        image.setAlignment(Qt.AlignCenter)
        
        # Player name
        name_label = QLabel(name)
        name_label.setFont(QFont("Roboto", 18, QFont.Weight.Bold))
        name_label.setStyleSheet("color: white;")
        name_label.setAlignment(Qt.AlignCenter)
        
        # Selection indicator
        select_label = QLabel("Click to select")
        select_label.setStyleSheet("color: #bdc3c7;")
        select_label.setAlignment(Qt.AlignCenter)
        
        # Add widgets to card layout
        card_layout.addWidget(image, alignment=Qt.AlignCenter)
        card_layout.addWidget(name_label)
        card_layout.addWidget(select_label)
        
        # Connect click event
        frame.mousePressEvent = lambda event, id=player_id: self.select_player(id, frame)
        
        return frame
    
    def select_player(self, player_id, frame):
        """Handle player selection and deselection"""
        # If clicking the already selected player, deselect it
        if self.selected_player == player_id:
            self.selected_player = None
            # Reset frame to original color
            if player_id == 0:
                frame.setStyleSheet("""
                    QFrame {
                        background-color: #f76c59;
                        border-radius: 15px;
                        padding: 15px;
                    }
                """)
            else:
                frame.setStyleSheet("""
                    QFrame {
                        background-color: #4382e8;
                        border-radius: 15px;
                        padding: 15px;
                    }
                """)
        else:
            self.selected_player = player_id
            # Update selected frame color
            if player_id == 0:
                frame.setStyleSheet("""
                    QFrame {
                        background-color: #f23f27;
                        border-radius: 15px;
                        padding: 15px;
                    }
                """)
            else:
                frame.setStyleSheet("""
                    QFrame {
                        background-color: #0033ea;
                        border-radius: 15px;
                        padding: 15px;
                    }
                """)
    
    def create_control_page(self):
        """Create the control page with instructions and buttons"""
        control_page = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Game Controls", control_page)
        title.setFont(QFont("Roboto", 32, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin: 20px;")
        
        # Instructions
        instructions = QLabel(
            "Welcome to YOLO Brawlers! Here's how to control your character:"
        )
        instructions.setFont(QFont("Roboto", 14))
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #34495e; margin: 10px;")
        
        # Instructions frame
        instructions_frame = QFrame()
        instructions_frame.setStyleSheet("""
            QFrame {
                background-color: #ecf0f1;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        instructions_layout = QVBoxLayout(instructions_frame)

        # WiFi network instruction
        wifi_network = "ESP32_Servo_Control_Red" if self.selected_player == 0 else "ESP32_Servo_Control_Blue"
        connection_instruction = QLabel(
            f"Connect to the {wifi_network} WiFi network to control your character.\n"
        )
        connection_instruction.setFont(QFont("Roboto", 14))
        connection_instruction.setWordWrap(True)
        connection_instruction.setStyleSheet("color: #34495e; margin: 10px;")
        instructions_layout.addWidget(connection_instruction)

        # Control instructions
        control_list = QLabel(
            "• Right Arrow - Toggle Toy 1 Trigger 1 (90⇄145 degrees)\n"
            "• Left Arrow  - Toggle Toy 1 Trigger 2 (90⇄145 degrees)\n"
            "• Up Arrow    - Guard\n"
            "• E Key       - Toggle Trigger 1\n"
            "• Q Key       - Toggle Trigger 2\n"
            "• ESC Key     - Exit"
        )
        control_list.setFont(QFont("Consolas", 14))
        control_list.setStyleSheet("color: #2c3e50;")
        
        instructions_layout.addWidget(control_list)
        
        # Chip type selection
        chip_group = QGroupBox("Select Chip Type for Camera")
        chip_group.setFont(QFont("Roboto", 16, QFont.Weight.Bold))
        chip_group.setStyleSheet("""
            QGroupBox {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 15px;
                margin-top: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px;
                color: #2c3e50;
            }
        """)
        
        chip_layout = QHBoxLayout()
        
        self.radio_chip_group = QButtonGroup(control_page)
        self.radio_chip_0 = QRadioButton("Intel/AMD")
        self.radio_chip_1 = QRadioButton("Apple Silicon")
        self.radio_chip_0.setFont(QFont("Roboto", 14))
        self.radio_chip_1.setFont(QFont("Roboto", 14))
        self.radio_chip_0.setChecked(True)
        self.radio_chip_group.addButton(self.radio_chip_0, 0)
        self.radio_chip_group.addButton(self.radio_chip_1, 1)
        
        chip_layout.addWidget(self.radio_chip_0)
        chip_layout.addWidget(self.radio_chip_1)
        chip_group.setLayout(chip_layout)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        # Keyboard controller button
        self.btn_keyboard = QPushButton("Start Keyboard Controller", control_page)
        self.btn_keyboard.setFont(QFont("Roboto", 14, QFont.Weight.Bold))
        self.btn_keyboard.setMinimumHeight(50)
        self.btn_keyboard.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        self.btn_keyboard.clicked.connect(self.start_keyboard_controller)
        
        # Camera button
        self.btn_camera = QPushButton("Open CV Camera", control_page)
        self.btn_camera.setFont(QFont("Roboto", 14, QFont.Weight.Bold))
        self.btn_camera.setMinimumHeight(50)
        self.btn_camera.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:pressed {
                background-color: #6c3483;
            }
        """)
        self.btn_camera.clicked.connect(self.open_camera)
        
        button_layout.addWidget(self.btn_keyboard)
        button_layout.addWidget(self.btn_camera)
        
        # Back button
        back_button = QPushButton("Back to Player Selection", control_page)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #7f8c8d;
                border: none;
                padding: 5px;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #2c3e50;
            }
        """)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        # Add widgets to layout
        layout.addWidget(title)
        layout.addWidget(instructions)
        layout.addWidget(instructions_frame)
        layout.addWidget(chip_group)
        layout.addStretch(1)
        layout.addLayout(button_layout)
        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)
        
        control_page.setLayout(layout)
        self.stacked_widget.addWidget(control_page)
    
    # Navigation methods
    def go_to_player_selection(self):
        self.stacked_widget.setCurrentIndex(1)
    
    def go_to_control_page(self):
        """Navigate to control page only if a player is selected"""
        if self.selected_player is not None:
            # Remove existing control page if it exists
            if self.stacked_widget.count() > 2:  # If we have more than start and player selection pages
                self.stacked_widget.removeWidget(self.stacked_widget.widget(2))
            
            # Create new control page with current player selection
            self.create_control_page()
            self.stacked_widget.setCurrentIndex(2)
        else:
            # Could add a message box here to inform user to select a player first
            pass
    
    # Action methods
    def start_keyboard_controller(self):
        """Starts the keyboard controller in a dialog."""
        try:
            from client.KeyboardController import KeyboardController
            from keyboard_controller_dialog import KeyboardControllerDialog
            
            # Pass the selected player ID to the controller
            self.controller = KeyboardController(toy_id=self.selected_player)
            dialog = KeyboardControllerDialog(self.controller, self)
            dialog.exec_()
            
        except Exception as e:
            print(f"Failed to start keyboard controller: {e}")
    
    def open_camera(self):
        """Opens the OpenCV camera with the selected settings."""
        try:
            is_apple_silicon = self.radio_chip_1.isChecked()
            # Implement your camera opening logic here
            print(f"Opening camera with settings: Player {self.selected_player}, Apple Silicon: {is_apple_silicon}")
            
        except Exception as e:
            print(f"Failed to open camera: {e}")
    
    def test_robot_connection(self):
        """Tests connection to the robot."""
        try:
            from client.KeyboardController import KeyboardController
            
            # Create temporary controller to test connection
            temp_controller = KeyboardController(toy_id=self.selected_player)
            success = temp_controller.test_connection()
            
            if success:
                self.connection_status.setText("Connected successfully!")
                self.connection_status.setStyleSheet("color: green;")
            else:
                self.connection_status.setText("Connection failed!")
                self.connection_status.setStyleSheet("color: red;")
            
            temp_controller.close()
            
        except Exception as e:
            self.connection_status.setText(f"Error: {str(e)}")
            self.connection_status.setStyleSheet("color: red;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())