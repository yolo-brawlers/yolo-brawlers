import socket
import struct
import time
from ml_model.yolo_fightingpose_detection import ZonePoseDetector, FightingPose

class ToyController:
    def __init__(self, host="192.168.4.1", port=8080, trigger1_pos=90, trigger2_pos=90, weave_pos=90, toy_id=0):
        self.host = host
        self.port = port
        self.socket = None

        self.toy_id = 1

        if self.toy_id == 0:  # Player 1
            self.trigger1_pos = 150
            self.set_servo(self.toy_id, 0, self.trigger1_pos)  # Starting position for trigger 1

            self.trigger2_pos = 30
            self.set_servo(self.toy_id, 1, self.trigger2_pos)  # Starting position for trigger 2 (left punch)

            self.weave_pos = 90
            self.weave = self.set_servo(self.toy_id, 2, self.weave_pos)  # Starting position should be guard
        else:  # Player 2
            self.trigger1_pos = 180
            self.set_servo(0, 0, self.trigger1_pos)  # Starting position for trigger 1

            self.trigger2_pos = 20
            self.set_servo(0, 1, self.trigger2_pos)  # Starting position for trigger 2 (left punch)

            self.weave_pos = 110
            self.weave = self.set_servo(0, 2, self.weave_pos)  # Starting position should be guard

        # Servo IDs
        self.servo_right_punch = 0
        self.servo_left_punch = 1
        self.servo_weave = 2
        print(f"Hola I'm robot {self.toy_id}")

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

    def toggle_trigger1(self):
        """Toggle Toy 1 Trigger 1 between 90 and 145 degrees"""
        if self.toy_id == 0:
            self.trigger1_pos = 90 if self.trigger1_pos == 150 else 150
        else:
            self.trigger1_pos = 130 if self.trigger1_pos == 180 else 180
        return self.set_servo(0, self.servo_right_punch, self.trigger1_pos)

    def toggle_trigger2(self):
        """Toggle Toy 1 Trigger 2 between 90 and 145 degrees"""
        if self.toy_id == 0:
            self.trigger2_pos = 80 if self.trigger2_pos == 30 else 30
        else:
            self.trigger2_pos = 70 if self.trigger2_pos == 20 else 20
        return self.set_servo(0, self.servo_left_punch, self.trigger2_pos)

    def weave_right(self):
        """Toggle Toy 1 Weave between 90 and 145 degrees"""
        if self.toy_id == 0:
            self.weave_pos = 45
        else:
            self.weave_pos = 65
        return self.set_servo(0, self.servo_weave, self.weave_pos)

    def weave_left(self):
        """Toggle Toy 1 Weave between 90 and 145 degrees"""
        if self.toy_id == 0:
            self.weave_pos = 135
        else:
            self.weave_pos = 135
        return self.set_servo(0, 2, self.weave_pos)

    def guard(self):
        """Toggle Toy 1 Weave between 90 and 145 degrees"""
        if self.toy_id == 0:
            self.weave_pos = 90
            self.set_servo(0, self.servo_right_punch, 150)
            self.set_servo(0, self.servo_left_punch, 30)

        else:
            self.weave_pos = 110
            self.set_servo(0, self.servo_right_punch, 180)
            self.set_servo(0, self.servo_left_punch, 20)

        return self.set_servo(0, self.servo_weave, self.weave_pos)
