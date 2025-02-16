import time
from yolo_fightingpose_detection import ZonePoseDetector, FightingPose
from controller import ToyController

# Initialize the pose detector and toy controller
detector = ZonePoseDetector()
controller = ToyController()

# Connect to the ESP32
if not controller.connect():
    print("Failed to connect to ESP32.")
    exit(1)

def handle_pose(pose):
    """Send appropriate servo commands based on detected pose."""
    if pose == FightingPose.PUNCH_RIGHT:
        controller.set_servo(0, 0, 90)  # Toy 1, Trigger 1, 90 degrees
        time.sleep(0.1)
        controller.set_servo(0, 0, 0)   # Back to 0 degrees
    elif pose == FightingPose.PUNCH_LEFT:
        controller.set_servo(0, 1, 90)  # Toy 1, Trigger 2, 90 degrees
        time.sleep(0.1)
        controller.set_servo(0, 1, 0)   # Back to 0 degrees
    elif pose == FightingPose.WEAVE_RIGHT:
        controller.set_servo(0, 2, 90)  # Toy 1, Weave, 90 degrees
    elif pose == FightingPose.WEAVE_LEFT:
        controller.set_servo(0, 2, 90)  # Toy 1, Weave, 90 degrees

    # Delay to prevent rapid-fire commands
    time.sleep(0.5)

def main():
    import cv2

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit(1)

    current_pose = None

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Detect the pose
            annotated_frame, pose = detector.process_frame(frame)

            # If a new pose is detected, act on it
            if pose and pose != current_pose:
                print(f"Detected pose: {pose.value}")
                current_pose = pose
                handle_pose(pose)

            # Display the annotated frame
            cv2.imshow("Fighting Pose Detection", annotated_frame)

            # Exit on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        controller.close()

if __name__ == "__main__":
    main()
