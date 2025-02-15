from ultralytics import YOLO
import cv2
import torch

# Load the YOLOv11 model
model = YOLO("yolo11n-pose.pt")  # Use 'yolo11n.pt' for the nano model

# Set device to MPS for Apple Silicon; fallback to CPU if unavailable
device = 'mps' if torch.backends.mps.is_available() else 'cpu'
model.to(device)

# Initialize camera
cap = cv2.VideoCapture(1) # Change 1 to 0 for Windows

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Run YOLOv11 inference
    results = model(frame, device=device)
    print(results)
    # Visualize results on the frame
    annotated_frame = results[0].plot()

    # Display the frame
    cv2.imshow("YOLOv11 Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
