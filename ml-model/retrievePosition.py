from ultralytics import YOLO
import cv2
import csv
import os
import sys

# Check for required command-line argument
if len(sys.argv) < 2:
    print("Usage: python script.py <file_suffix>")
    sys.exit(1)

file_suffix = sys.argv[1]

# File paths
csv_file = f"./pose_results/pose_results{file_suffix}.csv"
video_file = f"./video_results/video_results{file_suffix}.mp4"

# Ensure directories exist
os.makedirs("./pose_results", exist_ok=True)
os.makedirs("./video_results", exist_ok=True)

# Delete old files if they exist
if os.path.exists(csv_file):
    os.remove(csv_file)
    print(f"Deleted old CSV file: {csv_file}")

if os.path.exists(video_file):
    os.remove(video_file)
    print(f"Deleted old video file: {video_file}")

# Load YOLO Pose model
model = YOLO("yolo11n-pose.pt")  # Ensure correct model filename

# Open camera
cap = cv2.VideoCapture(0)  

# Get default frame width and height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS)) if cap.get(cv2.CAP_PROP_FPS) > 0 else 30  # Default to 30 FPS if unknown

print(f"Recording at {frame_width}x{frame_height}, {fps} FPS")

# Keypoint mapping using COCO format (Body Part -> Index)
keypoint_mapping = {
    "Nose": 0, "Left Eye": 1, "Right Eye": 2, "Left Ear": 3, "Right Ear": 4,
    "Left Shoulder": 5, "Right Shoulder": 6, "Left Elbow": 7, "Right Elbow": 8,
    "Left Wrist": 9, "Right Wrist": 10, "Left Hip": 11, "Right Hip": 12,
    "Left Knee": 13, "Right Knee": 14, "Left Ankle": 15, "Right Ankle": 16
}

# Define OpenCV VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter(video_file, fourcc, fps, (frame_width, frame_height))

# Open CSV file for writing results
with open(csv_file, mode="w", newline="") as file:
    writer = csv.writer(file)

    # Write CSV header
    header = ["Frame"] + list(keypoint_mapping.keys())
    writer.writerow(header)

    frame_count = 0
    max_frames = 50  # Save up to 50 frames

    # Run while camera is open and frame count has not exceeded 50
    while cap.isOpened() and frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        # Run inference
        results = model(frame, device="cpu")  # Use 'cpu' due to MPS Pose bug
        
        for result in results:
            keypoints = result.keypoints.xy  # Extract keypoints
            
            for person in keypoints:  # Loop through detected people
                keypoint_data = [frame_count]
                
                for body_part, index in keypoint_mapping.items():
                    if index < len(person):  # Ensure index is within range
                        keypoint = person[index].tolist()
                        keypoint_data.append(f"({int(keypoint[0])}, {int(keypoint[1])})")
                    else:
                        keypoint_data.append("N/A")  # If no detection

                writer.writerow(keypoint_data)

        # Annotate frame number (top right)
        text = f"Frame: {frame_count}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_thickness = 2
        text_color = (255, 255, 255)  # White

        # Get text size to position it dynamically
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        text_x = frame_width - text_size[0] - 20  # 20px margin from right
        text_y = 50  # 50px from top

        cv2.putText(frame, text, (text_x, text_y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

        frame_count += 1

        # Save frame to output video (MP4)
        output_video.write(frame)

        # Show frame
        cv2.imshow("YOLO 11 Pose Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
output_video.release()
cv2.destroyAllWindows()
print(f"Saved video: {video_file}")
print(f"Saved CSV data: {csv_file}")
