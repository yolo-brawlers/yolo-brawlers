import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QKeyEvent

class KeyboardControllerDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Keyboard Control Mode")
        self.setGeometry(150, 150, 400, 300)
        
        # Layout
        layout = QVBoxLayout()
        
        # Instructions
        title = QLabel("Keyboard Control Mode")
        title.setFont(QFont("Roboto", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        
        instructions = QLabel(
            "Commands:\n"
            "  Right Arrow - Toggle Toy 1 Trigger 1 (90⇄145 degrees)\n"
            "  Left Arrow  - Toggle Toy 1 Trigger 2 (90⇄145 degrees)\n"
            "  Up Arrow    - Guard\n"
            "  E           - Toggle Trigger 1\n"
            "  Q           - Toggle Trigger 2\n"
            "  ESC         - Exit"
        )
        instructions.setAlignment(Qt.AlignLeft)
        instructions.setFont(QFont("Consolas", 12))
        
        # Exit button
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        
        # Add widgets to layout
        layout.addWidget(title)
        layout.addWidget(instructions)
        layout.addWidget(exit_button)
        
        self.setLayout(layout)
        
        # Set focus to receive key events
        self.setFocusPolicy(Qt.StrongFocus)
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Right:
            self.controller.weave_right()
        elif event.key() == Qt.Key_Left:
            self.controller.weave_left()
        elif event.key() == Qt.Key_Up:
            self.controller.guard()
        elif event.key() == Qt.Key_E:
            self.controller.toggle_trigger1()
        elif event.key() == Qt.Key_Q:
            self.controller.toggle_trigger2()
        elif event.key() == Qt.Key_Escape:
            self.close()
        
        # Don't call super() to avoid closing dialog on Escape
    
    def closeEvent(self, event):
        # Clean up resources when the dialog is closed
        try:
            self.controller.close()
        except Exception as e:
            print(f"Error closing controller: {e}")
        event.accept()