import socket
import struct
import time
from yolo_fightingpose_detection import ZonePoseDetector, FightingPose

class ToyController:
    """
    Controls a toy robot using servo motors via a network connection.

    This class:
    - Connects to a toy robot over WiFi using a socket.
    - Sends servo motor control commands to the toy robot.
    - Handles errors and reconnections if needed.

    Attributes:
        host (str): IP address of the toy's ESP32 module.
        port (int): Port number for the network connection.
        socket (socket.socket): TCP socket for communication.
    """

    def __init__(self, host="192.168.4.1", port=8080):
        """
        Initializes the ToyController with the target IP and port.

        Args:
            host (str, optional): IP address of the toy. Defaults to "192.168.4.1".
            port (int, optional): Port number for communication. Defaults to 8080.
        """
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        """
        Establishes a TCP connection with the toy's ESP32 module.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5.0)
            self.socket.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def set_servo(self, toy_id, servo_type, angle):
        """
        Sends a command to control a specific servo motor.

        Args:
            toy_id (int): 0 for Toy 1, 1 for Toy 2.
            servo_type (int): 0 for Trigger 1, 1 for Trigger 2, 2 for Weave movement.
            angle (int): Angle between 0 and 180 degrees.

        Returns:
            bool: True if the command was successfully sent, False otherwise.
        """
        if not self.socket:
            if not self.connect():
                return False

        try:
            data = struct.pack("BBB", toy_id, servo_type, angle)
            self.socket.send(data)
            response = self.socket.recv(2)

            if response == b"OK":
                servo_names = ["Trigger1", "Trigger2", "Weave"]
                print(f"Toy{toy_id + 1} {servo_names[servo_type]} set to {angle} degrees")
                return True
            return False
        except Exception as e:
            print(f"Failed to set servo: {e}")
            self.socket = None
            return False

    def close(self):
        """
        Closes the connection to the toy's ESP32 module.
        """
        if self.socket:
            self.socket.close()
            self.socket = None

'''
def interactive_control():
    """
    Provides an interactive terminal interface to manually control servos.

    - Users can enter commands to control different toy movements.
    - Example commands:
        - `toy1_t1:90` → Moves Toy 1's Trigger 1 servo to 90 degrees.
        - `toy2_w:180` → Moves Toy 2's Weave servo to 180 degrees.
        - `quit` → Exits the program.
    """
    controller = ToyController()

    print("Interactive Servo Control")
    print("Commands:")
    print("  toy1_t1:angle - Set Toy 1 Trigger 1")
    print("  toy1_t2:angle - Set Toy 1 Trigger 2")
    print("  toy1_w:angle  - Set Toy 1 Weave")
    print("  toy2_t1:angle - Set Toy 2 Trigger 1")
    print("  toy2_t2:angle - Set Toy 2 Trigger 2")
    print("  toy2_w:angle  - Set Toy 2 Weave")
    print("  quit - Exit program")

    try:
        while True:
            command = input("\nEnter command: ").strip().lower()

            if command == "quit":
                break

            parts = command.split(":")
            if len(parts) != 2:
                print("Invalid command format. Use prefix:angle")
                continue

            prefix, angle_str = parts
            try:
                angle = int(angle_str)
                if angle < 0 or angle > 180:
                    print("Angle must be between 0 and 180")
                    continue
            except ValueError:
                print("Invalid angle value")
                continue

            # Parse command prefix
            if prefix.startswith("toy1_"):
                toy_id = 0
            elif prefix.startswith("toy2_"):
                toy_id = 1
            else:
                print("Invalid toy prefix")
                continue

            if prefix.endswith("_t1"):
                servo_type = 0
            elif prefix.endswith("_t2"):
                servo_type = 1
            elif prefix.endswith("_w"):
                servo_type = 2
            else:
                print("Invalid servo type")
                continue

            controller.set_servo(toy_id, servo_type, angle)

    finally:
        controller.close()
'''

if __name__ == "__main__":
    """
    Entry point for running the interactive servo control program.

    When executed directly, this script starts an interactive command-line interface
    allowing users to control servos manually.
    """
    # interactive_control()
    print("I'm a module!")
