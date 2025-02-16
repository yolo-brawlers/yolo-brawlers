# Modified Python client (gpio_controller.py)
import socket
import struct
import time


class GPIOController:
    def __init__(self, host="192.168.4.1", port=8080):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5.0)  # Add timeout
            self.socket.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def set_servo(self, servo_number, angle):
        if not self.socket:
            if not self.connect():
                return False

        try:
            data = struct.pack("BBB", 0xFF, servo_number, angle)
            self.socket.send(data)

            # Wait for acknowledgment
            response = self.socket.recv(2)
            if response == b"OK":
                print(f"Servo {servo_number} set to {angle} degrees")
                return True
            return False

        except Exception as e:
            print(f"Failed to set servo: {e}")
            self.socket = None
            return False

    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None


# Example usage
if __name__ == "__main__":
    controller = GPIOController()

    try:
        # Set servo 0 to 90 degrees
        if controller.set_servo(0, 180):
            print("Command successful")
        else:
            print("Command failed")

        # Add a small delay before closing
        time.sleep(0.1)

    finally:
        controller.close()
