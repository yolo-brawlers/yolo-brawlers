import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
import subprocess
import platform

class WifiInfoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WiFi Network Info")
        self.setGeometry(100, 100, 400, 200)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create label to display WiFi info
        self.wifi_label = QLabel("Checking WiFi...")
        layout.addWidget(self.wifi_label)
        
        # Get and display WiFi info
        self.update_wifi_info()
    
    def get_wifi_name(self):
        try:
            if platform.system() == "Windows":
                # For Windows
                cmd = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'])
                cmd = cmd.decode('utf-8', errors='ignore')
                for line in cmd.split('\n'):
                    if "SSID" in line and "BSSID" not in line:
                        return line.split(":")[1].strip()
            
            elif platform.system() == "Darwin":  # macOS
                cmd = subprocess.check_output(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'])
                cmd = cmd.decode('utf-8', errors='ignore')
                for line in cmd.split('\n'):
                    if " SSID" in line:
                        return line.split(": ")[1].strip()
            
            elif platform.system() == "Linux":
                cmd = subprocess.check_output(['iwgetid', '-r'])
                return cmd.decode('utf-8').strip()
                
            return "Not connected"
            
        except Exception as e:
            return f"Error getting WiFi name: {str(e)}"
    
    def update_wifi_info(self):
        wifi_name = self.get_wifi_name()
        self.wifi_label.setText(f"Current WiFi Network: {wifi_name}")

def main():
    app = QApplication(sys.argv)
    window = WifiInfoWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()