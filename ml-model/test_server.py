import socket
import struct
import time

class GPIOController:
    def __init__(self, host='192.168.4.1', port=8080):
        """
        Initialize GPIO controller client
        host: ESP32 WiFi AP address (default is typically 192.168.4.1)
        port: Port number for socket communication
        """
        self.host = host
        self.port = port
        self.socket = None
    
    def connect(self):
        """Establish connection to ESP32"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def set_pin(self, pin_number, value):
        """
        Set GPIO pin value
        pin_number: GPIO pin number
        value: 1 for HIGH, 0 for LOW
        """
        if not self.socket:
            if not self.connect():
                return False
        
        try:
            # Pack data: pin number (1 byte) + value (1 byte)
            data = struct.pack('BB', pin_number, value)
            self.socket.send(data)
            return True
        except Exception as e:
            print(f"Failed to set pin: {e}")
            self.socket = None
            return False
    
    def set_servo(self, servo_number, angle):
        """
        Set servo position
        servo_number: Servo identifier
        angle: Angle in degrees (0-180)
        """
        if not self.socket:
            if not self.connect():
                return False
        
        try:
            # Pack data: command type (1 byte) + servo number (1 byte) + angle (1 byte)
            data = struct.pack('BBB', 0xFF, servo_number, angle)
            self.socket.send(data)
            return True
        except Exception as e:
            print(f"Failed to set servo: {e}")
            self.socket = None
            return False
    
    def close(self):
        """Close the connection"""
        if self.socket:
            self.socket.close()
            self.socket = None

# Example usage
if __name__ == "__main__":
    controller = GPIOController()
    
    print("starting")
    # Example: Control GPIO pins
    controller.set_pin(2, 1)  # Set GPIO2 HIGH
    time.sleep(1)
    controller.set_pin(2, 0)  # Set GPIO2 LOW
    
    # Example: Control servos
    controller.set_servo(1, 90)  # Set servo 1 to 90 degrees
    
    controller.close()