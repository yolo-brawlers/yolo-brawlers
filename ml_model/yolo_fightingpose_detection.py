"""
YOLO Fighting Pose Detection Module

This module:
- Uses YOLOv11 for pose detection.
- Identifies and classifies different fighting poses.
- Determines position zones (left, right, center).
- Applies temporal smoothing for better pose classification.

Classes:
    - FightingPose: Enum class defining possible fighting stances.
    - ZonePoseDetector: Class that processes frames and detects poses.

Author: [Your Name]
"""

from ultralytics import YOLO
import cv2
import torch
from enum import Enum
import numpy as np
import sys
from typing import Optional
sys.path.append("../")

class FightingPose(Enum):
    """
    Enum class representing different fighting poses.
    """
    GUARD = "guard"
    WEAVE_RIGHT = "weave_right"
    WEAVE_LEFT = "weave_left"
    PUNCH_RIGHT = "punch_right"
    PUNCH_LEFT = "punch_left"

class ZonePoseDetector:
    """
    Detects fighting poses using YOLOv11.

    This class:
    - Loads a YOLO model for pose detection.
    - Classifies fighting poses based on detected keypoints.
    - Divides the screen into three zones (left, center, right).
    - Implements smoothing to avoid rapid pose switching.

    Attributes:
        model (YOLO): The loaded YOLOv11 model for pose detection.
        device (str): The computing device (MPS for Apple Silicon, else CPU).
        left_boundary (int): Left boundary of the center zone.
        right_boundary (int): Right boundary of the center zone.
        buffer_percentage (float): Small buffer zone percentage to prevent jitter.
        pose_history (list): Stores recent poses for smoothing.
        history_length (int): Number of frames considered for pose smoothing.
    """

    def __init__(self):
        # Load the YOLOv11 model
        self.model = YOLO("../model_assets/yolo11n-pose.pt")
        # Set device to MPS for Apple Silicon; fallback to CPU if unavailable
        self.device = 'mps' if torch.backends.mps.is_available() else 'cpu'
        self.model.to(self.device)

        self.left_boundary = None
        self.right_boundary = None
        self.buffer_percentage = 0.0  # Prevents rapid zone switching

        # Smoothing setup
        self.pose_history = []
        self.history_length = 3

    def setup_zones(self, frame_width):
        """
        Sets up the left, right, and center zone boundaries based on frame width.

        The center zone occupies 40% of the frame width, while the left and right zones
        each take up 30%.

        Args:
            frame_width (int): Width of the input frame.
        """
        middle_zone_width = int(frame_width * 0.36)
        side_zone_width = (frame_width - middle_zone_width) // 2

        self.left_boundary = side_zone_width
        self.right_boundary = frame_width - side_zone_width

        # Calculate buffer zones
        self.buffer = int(frame_width * self.buffer_percentage)

    def draw_zones(self, frame):
        """
        Draws visual markers for the left, center, and right zones.

        Args:
            frame (numpy.ndarray): The input frame on which zones are drawn.
        """
        height = frame.shape[0]

        cv2.line(frame, (self.left_boundary, 0), (self.left_boundary, height), (0, 255, 0), 2)
        cv2.line(frame, (self.right_boundary, 0), (self.right_boundary, height), (0, 255, 0), 2)

    def get_zone(self, x_position):
        """
        Determines which zone a given x-coordinate falls into.

        Args:
            x_position (int): X-coordinate of the detected point.

        Returns:
            str: "left", "right", or "center", or None if in buffer zone.
        """
        if x_position < (self.left_boundary - self.buffer):
            return "left"
        elif x_position > (self.right_boundary + self.buffer):
            return "right"
        elif self.left_boundary + self.buffer <= x_position <= self.right_boundary - self.buffer:
            return "center"
        return None  # Buffer zone

    def get_face_position(self, keypoints):
        """
        Calculates the average x-position of the detected face.

        Args:
            keypoints (numpy.ndarray): The detected keypoints.

        Returns:
            float: The average x-coordinate of the face.
        """
        nose, left_eye, right_eye = keypoints[:3]
        return np.mean([nose[0], left_eye[0], right_eye[0]])

    def smooth_pose(self, new_pose):
        """
        Applies temporal smoothing to detected poses to prevent flickering.

        Args:
            new_pose (FightingPose): The newly detected pose.

        Returns:
            FightingPose: The smoothed pose.
        """
        self.pose_history.append(new_pose)
        if len(self.pose_history) > self.history_length:
            self.pose_history.pop(0)

        return new_pose if len(set(self.pose_history)) == 1 else self.pose_history[0]

    def classify_pose(self, keypoints) -> Optional[FightingPose]:
        """
        Classifies the detected pose based on keypoints.

        Args:
            keypoints (numpy.ndarray): Array of detected keypoints.

        Returns:
            Optional[FightingPose]: The classified fighting pose, or None if undetermined.
        """
        if keypoints is None or len(keypoints) == 0:
            return None

        face_x = self.get_face_position(keypoints)
        left_wrist, right_wrist = keypoints[9], keypoints[10]

        face_zone = self.get_zone(face_x)
        left_hand_zone = self.get_zone(left_wrist[0])
        right_hand_zone = self.get_zone(right_wrist[0])

        # Prioritize punches over weaves
        if left_hand_zone == "right":
            return FightingPose.PUNCH_RIGHT
        if right_hand_zone == "left":
            return FightingPose.PUNCH_LEFT

        if face_zone == "left":
            return FightingPose.WEAVE_LEFT
        elif face_zone == "right":
            return FightingPose.WEAVE_RIGHT

        return FightingPose.GUARD  # Default to guard position

    def process_frame(self, frame):
        """
        Processes an input frame and detects the fighting pose.

        - Runs YOLO inference to detect keypoints.
        - Classifies the pose based on detected keypoints.
        - Applies smoothing to the detected pose.
        - Annotates the frame with detected keypoints and pose label.

        Args:
            frame (numpy.ndarray): The input image frame.

        Returns:
            tuple: Annotated frame (numpy.ndarray), detected pose (Optional[FightingPose]).
        """
        if self.left_boundary is None:
            self.setup_zones(frame.shape[1])

        self.draw_zones(frame)
        results = self.model(frame, device=self.device)

        if len(results) > 0 and len(results[0].keypoints) > 0:
            keypoints = results[0].keypoints[0].xy.cpu().numpy()[0]
            raw_pose = self.classify_pose(keypoints)
            smoothed_pose = self.smooth_pose(raw_pose)

            # Visualize results
            annotated_frame = results[0].plot()
            self.draw_zones(annotated_frame)

            if smoothed_pose:
                cv2.putText(
                    annotated_frame, f"Pose: {smoothed_pose.value}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
                )

            return annotated_frame, smoothed_pose

        return frame, None

if __name__ == "__main__":
    """
    This script is meant to be imported, not executed directly.
    """
    print("This script is meant to be imported, not run directly.")
