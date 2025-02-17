from PoseController import PoseController
from ml_model.yolo_fightingpose_detection import ZonePoseDetector 
from KeyboardController import KeyboardController
import sys
import os



def main():
    mode = input("Choose mode (yolo/keyboard): ").strip().lower()

    if mode == "yolo":
        controller = PoseController()
        if controller.connect():
            controller.run_yolo_mode()
        else:
            print("Failed to connect to ESP32.")
    elif mode == "keyboard":
        controller = KeyboardController(toy_id=0)  # arg cli
        if controller.connect():
            controller.run_keyboard_mode()
        else:
            print("Failed to connect to ESP32.")

    elif mode == "test":
        model = ZonePoseDetector()
    else:
        print("Invalid mode. Choose 'yolo' or 'keyboard'.")

if __name__ == "__main__":
    main()
