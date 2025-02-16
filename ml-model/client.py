import socket
import struct
import time
from yolo_fightingpose_detection import ZonePoseDetector, FightingPose
s



class ToyController:
    def __init__(self, host="192.168.4.1", port=8080):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
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
        Control a specific servo
        toy_id: 0 for toy1, 1 for toy2
        servo_type: 0 for trigger1, 1 for trigger2, 2 for weave
        angle: 0-180
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
        if self.socket:
            self.socket.close()
            self.socket = None


def interactive_control():
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


if __name__ == "__main__":
    interactive_control()
