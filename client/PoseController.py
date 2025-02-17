import time
import sys
import cv2

sys.path.append("../")
from ml_model.yolo_fightingpose_detection import ZonePoseDetector, FightingPose
from controller import ToyController

class PoseController(ToyController):
    def __init__(self, host="192.168.4.1", port=8080):
        super().__init__(host, port)
        self.detector = ZonePoseDetector()

    def handle_pose(self, pose):
        """Send appropriate servo commands based on detected pose."""
        if pose == FightingPose.PUNCH_RIGHT:
            self.toggle_trigger1()
        elif pose == FightingPose.PUNCH_LEFT:
            self.toggle_trigger2()
        elif pose == FightingPose.WEAVE_RIGHT:
            self.weave_right()
        elif pose == FightingPose.WEAVE_LEFT:
            self.weave_left()
        elif pose == FightingPose.GUARD:
            self.guard()