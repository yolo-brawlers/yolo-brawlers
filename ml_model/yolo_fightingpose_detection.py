from ultralytics import YOLO
import cv2
import torch
from enum import Enum
import numpy as np
import sys
from typing import Optional
sys.path.append("../")

class FightingPose(Enum):
    GUARD = "guard"
    WEAVE_RIGHT = "weave_right"
    WEAVE_LEFT = "weave_left"
    PUNCH_RIGHT = "punch_right"
    PUNCH_LEFT = "punch_left"

class ZonePoseDetector:
    def __init__(self):
        # Load the YOLOv11 model
        self.model = YOLO("../model_assets/yolo11n-pose.pt")
        # Set device to MPS for Apple Silicon; fallback to CPU if unavailable
        self.device = 'mps' if torch.backends.mps.is_available() else 'cpu'
        self.model.to(self.device)
        
        # Initialize zone boundaries (will be set when first frame is processed)
        self.left_boundary = None
        self.right_boundary = None
        
        # Add a small buffer zone to prevent rapid switching
        self.buffer_percentage = 0.0
        
        # Add pose smoothing
        self.pose_history = []
        self.history_length = 3  # Number of frames to consider for smoothing

    def setup_zones(self, frame_width):
        """Setup the zone boundaries based on frame width with wider middle zone"""
        # Make middle zone 40% of frame width, leaving 30% for side zones
        middle_zone_width = int(frame_width * 0.4)
        side_zone_width = (frame_width - middle_zone_width) // 2
        
        self.left_boundary = side_zone_width
        self.right_boundary = frame_width - side_zone_width
        
        # Calculate buffer zones
        self.buffer = int(frame_width * self.buffer_percentage)

    def draw_zones(self, frame):
        """Draw zone boundaries on the frame"""
        height = frame.shape[0]
        
        # Draw main zone lines
        cv2.line(frame, (self.left_boundary, 0), (self.left_boundary, height), (0, 255, 0), 2)
        cv2.line(frame, (self.right_boundary, 0), (self.right_boundary, height), (0, 255, 0), 2)
        
        # Buffer zone visualization (commented out)
        # cv2.line(frame, (self.left_boundary - self.buffer, 0), 
        #         (self.left_boundary - self.buffer, height), (0, 255, 0), 1)
        # cv2.line(frame, (self.left_boundary + self.buffer, 0), 
        #         (self.left_boundary + self.buffer, height), (0, 255, 0), 1)
        # cv2.line(frame, (self.right_boundary - self.buffer, 0), 
        #         (self.right_boundary - self.buffer, height), (0, 255, 0), 1)
        # cv2.line(frame, (self.right_boundary + self.buffer, 0), 
        #         (self.right_boundary + self.buffer, height), (0, 255, 0), 1)

    def get_zone(self, x_position):
        """Determine which zone a point is in, considering buffer zones"""
        if x_position < (self.left_boundary - self.buffer):
            return "left"
        elif x_position > (self.right_boundary + self.buffer):
            return "right"
        elif self.left_boundary + self.buffer <= x_position <= self.right_boundary - self.buffer:
            return "center"
        return None  # Point is in a buffer zone

    def get_face_position(self, keypoints):
        """Calculate average position of facial features"""
        # Get facial keypoints (nose and eyes)
        nose = keypoints[0]
        left_eye = keypoints[1]
        right_eye = keypoints[2]
        
        # Calculate average x position
        face_x = np.mean([nose[0], left_eye[0], right_eye[0]])
        
        return face_x

    def smooth_pose(self, new_pose):
        """Apply temporal smoothing to pose detection"""
        self.pose_history.append(new_pose)
        if len(self.pose_history) > self.history_length:
            self.pose_history.pop(0)
        
        # Only change pose if we have consistent readings
        if len(set(self.pose_history)) == 1:
            return new_pose
        return self.pose_history[0]  # Return the oldest pose if inconsistent

    def classify_pose(self, keypoints) -> Optional[FightingPose]:
        """Classify the fighting pose based on face and hand positions"""
        if keypoints is None or len(keypoints) == 0:
            return None
            
        # Get average face position
        face_x = self.get_face_position(keypoints)
        
        # Get hand positions
        left_wrist = keypoints[9]
        right_wrist = keypoints[10]
        
        # Get zones for face and hands
        face_zone = self.get_zone(face_x)
        left_hand_zone = self.get_zone(left_wrist[0])
        right_hand_zone = self.get_zone(right_wrist[0])
        
        # Check for punches first (they take precedence over weaves)
        # Then check for weaves
        if face_zone == "left":
            return FightingPose.WEAVE_LEFT
        elif face_zone == "right":
            return FightingPose.WEAVE_RIGHT
        
        if left_hand_zone == "right":
            return FightingPose.PUNCH_RIGHT
        elif right_hand_zone == "left":
            return FightingPose.PUNCH_LEFT
        # elif left_hand_zone == "right" and right_hand_zone == "right":
        #     return FightingPose.WEAVE_RIGHT
        # elif left_hand_zone == "left" and right_hand_zone == "left":
        #     return FightingPose.WEAVE_LEFT
        
        
        # Default to guard if in center or buffer zones
        return FightingPose.GUARD

    def process_frame(self, frame):
        """Process a single frame and return the detected pose"""
        # Setup zones if not already done
        if self.left_boundary is None:
            self.setup_zones(frame.shape[1])
        
        # Draw zones on frame
        self.draw_zones(frame)
        
        # Run YOLOv11 inference
        results = self.model(frame, device=self.device)
        
        # Get keypoints from the first detected person
        if len(results) > 0 and len(results[0].keypoints) > 0:
            keypoints = results[0].keypoints[0].xy.cpu().numpy()[0]
            
            # Classify and smooth pose
            raw_pose = self.classify_pose(keypoints)
            smoothed_pose = self.smooth_pose(raw_pose)
            
            # Visualize results
            annotated_frame = results[0].plot()
            self.draw_zones(annotated_frame)
            
            # Add pose classification text
            if smoothed_pose:
                cv2.putText(annotated_frame, f"Pose: {smoothed_pose.value}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
            return annotated_frame, smoothed_pose
            
        return frame, None

def main():
    detector = ZonePoseDetector()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()
    
    current_pose = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
        
        # Process frame and get pose
        annotated_frame, pose = detector.process_frame(frame)
        
        # Update current pose if a new pose is detected
        if pose is not None:
            if pose != current_pose:  # Only print when pose changes
                current_pose = pose
                print(f"Current pose: {current_pose.value}")
        
        # Display the frame
        cv2.imshow("Fighting Pose Detection", annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()