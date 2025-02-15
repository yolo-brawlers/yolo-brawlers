from ultralytics import YOLO
import cv2

# Load YOLO Pose model
model = YOLO("yolo11n-pose.pt")  # Ensure correct model filename

# Open camera
cap = cv2.VideoCapture(1) # 

keypoint_mapping = {
    0: "Nose",
    1: "Left Eye",
    2: "Right Eye",
    3: "Left Ear",
    4: "Right Ear",
    5: "Left Shoulder",
    6: "Right Shoulder",
    7: "Left Elbow",
    8: "Right Elbow",
    9: "Left Wrist",
    10: "Right Wrist",
    11: "Left Hip",
    12: "Right Hip",
    13: "Left Knee",
    14: "Right Knee",
    15: "Left Ankle",
    16: "Right Ankle"
}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run inference
    results = model(frame, device="cpu")  # Use 'cpu' due to MPS Pose bug
    for result in results:
        keypoints = result.keypoints.xy  # Extract keypoints

        for person in keypoints:  # Loop through detected people
            # Convert keypoints to integer tuples (x, y)
            left_shoulder = tuple(map(int, person[5].tolist()))
            right_shoulder = tuple(map(int, person[6].tolist()))
            left_hand = tuple(map(int, person[9].tolist()))
            right_hand = tuple(map(int, person[10].tolist()))

            # Draw keypoints
            cv2.circle(frame, left_shoulder, 20, (0, 255, 0), -1)  # Green
            cv2.circle(frame, right_shoulder, 20, (255, 0, 0), -1)  # Blue
            cv2.circle(frame, left_hand, 20, (0, 0, 255), -1)  # Red
            cv2.circle(frame, right_hand, 20, (255, 255, 0), -1)  # Yellow

    # Show frame
    cv2.imshow("YOLO 11 Pose Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
