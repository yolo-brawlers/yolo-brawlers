import socket
import struct
import time
import keyboard
import sys


class ToyController:
    def __init__(self, host="192.168.4.1", port=8080):
        self.host = host
        self.port = port
        self.socket = None
        # Track current positions
        self.toy1_t1_pos = 90  # Starting position for trigger 1
        self.toy1_t2_pos = 70  # Starting position for trigger 2

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
        angle: varies by toy and servo type:
            toy1_t1: 90-145 degrees
            toy1_t2: 35-90 degrees
            toy2: 0-180 degrees (all servos)
        """
        # Check angle restrictions for toy1
        if toy_id == 0:  # toy1
            if servo_type == 0:  # trigger1
                if angle < 90 or angle > 145:
                    print("Toy 1 Trigger 1 angle must be between 90 and 145 degrees")
                    return False
            elif servo_type == 1:  # trigger2
                if angle > 70 or angle < 20:
                    print("Toy 1 Trigger 2 angle must be between 90 and 145 degrees")
                    return False

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

    def toggle_toy1_t1(self):
        """Toggle Toy 1 Trigger 1 between 90 and 145 degrees"""
        self.toy1_t1_pos = 145 if self.toy1_t1_pos == 90 else 90
        return self.set_servo(0, 0, self.toy1_t1_pos)

    def toggle_toy1_t2(self):
        """Toggle Toy 1 Trigger 2 between 90 and 145 degrees"""
        self.toy1_t2_pos = 20 if self.toy1_t2_pos == 70 else 70
        return self.set_servo(0, 1, self.toy1_t2_pos)


def keyboard_control():
    controller = ToyController()
    print("Keyboard Control Mode")
    print("Commands:")
    print("  Right Arrow - Toggle Toy 1 Trigger 1 (90⇄145 degrees)")
    print("  Left Arrow  - Toggle Toy 1 Trigger 2 (90⇄145 degrees)")
    print("  ESC        - Exit program")

    try:
        # Set up keyboard event handlers
        keyboard.on_press_key("right", lambda _: controller.toggle_toy1_t1())
        keyboard.on_press_key("left", lambda _: controller.toggle_toy1_t2())
        keyboard.on_press_key("esc", lambda _: sys.exit(0))

        # Keep the program running
        keyboard.wait("esc")

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        controller.close()


if __name__ == "__main__":
    keyboard_control()
