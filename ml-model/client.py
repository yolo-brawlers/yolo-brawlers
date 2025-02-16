import time
from yolo_fightingpose_detection import ZonePoseDetector, FightingPose
from controller import Toytoy_Controller

def handle_pose(pose, toy_controller : Toytoy_Controller):
    """Send appropriate servo commands based on detected pose."""
    if pose == FightingPose.PUNCH_RIGHT:
        toy_controller.set_servo(0, 0, 90)  # Toy 1, Trigger 1, 90 degrees
        time.sleep(0.1)
        toy_controller.set_servo(0, 0, 0)   # Back to 0 degrees
    elif pose == FightingPose.PUNCH_LEFT:
        toy_controller.set_servo(0, 1, 90)  # Toy 1, Trigger 2, 90 degrees
        time.sleep(0.1)
        toy_controller.set_servo(0, 1, 0)   # Back to 0 degrees
    elif pose == FightingPose.WEAVE_RIGHT:
        toy_controller.set_servo(0, 2, 90)  # Toy 1, Weave, 90 degrees
    elif pose == FightingPose.WEAVE_LEFT:
        toy_controller.set_servo(0, 2, 180)  # Toy 1, Weave, -90 degrees
        # TODO: The angle is probably wrong, adjust as needed
    elif pose == FightingPose.GUARD:
        toy_controller.set_servo(0, 2, 0) # Toy 1, weave back to the center

    # Delay to prevent rapid-fire commands
    time.sleep(0.5)

if __name__ == "__main__":
    print("I'm a module!")
