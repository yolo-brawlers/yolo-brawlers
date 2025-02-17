import time
import sys
import cv2

sys.path.append("../")
from ml_model.yolo_fightingpose_detection import ZonePoseDetector, FightingPose
from controller import ToyController

class PoseController(ToyController):
    def __init__(self, host="192.168.4.1", port=8080, toy_id=0):
        super().__init__(host, port, toy_id)
        self.detector = ZonePoseDetector()

    def handle_pose(self, pose):
        """Send appropriate servo commands based on detected pose."""
        if pose == FightingPose.PUNCH_RIGHT:
            self.toggle_trigger1()
            # self.toggle_trigger1()
        elif pose == FightingPose.PUNCH_LEFT:
            self.toggle_trigger2()
            # self.toggle_trigger2()
        elif pose == FightingPose.WEAVE_RIGHT:
            self.weave_right()
        elif pose == FightingPose.WEAVE_LEFT:
            self.weave_left()
        elif pose == FightingPose.GUARD:
            self.guard()

    def run_yolo_mode(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            sys.exit(1)

        current_pose = None

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Failed to capture frame.")
                    break

                annotated_frame, pose = self.detector.process_frame(frame)

                if pose and pose != current_pose:
                    print(f"Detected pose: {pose.value}")
                    current_pose = pose
                    self.handle_pose(pose)

                cv2.imshow("Fighting Pose Detection", annotated_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            cap.release()
            cv2.destroyAllWindows()