from ultralytics import YOLO
import cv2
import torch
import requests
import time
import sys

# ESP32 configuration
ESP32_URL = "http://192.168.4.1"  # Default AP IP address
CONTROL_ENDPOINT = f"{ESP32_URL}/control"


def test_esp32_connection(max_retries=3):
    print("\nTesting connection to ESP32...")
    print(f"Attempting to connect to {ESP32_URL}")

    for attempt in range(max_retries):
        try:
            response = requests.get(ESP32_URL, timeout=2)
            print(f"Successfully connected to ESP32! (Attempt {attempt + 1})")
            print(f"Response: {response.text}\n")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed:")
            print(f"Error: {str(e)}")
            if attempt < max_retries - 1:
                print("Retrying in 2 seconds...")
                time.sleep(2)
            else:
                print("\nConnection failed after all attempts.")
                print("Please check:")
                print("1. ESP32 is powered on and running")
                print("2. Your computer is connected to 'ESP32-Robot-AP' WiFi network")
                print("3. The WiFi password is '12345678'")
                print("4. Try to access http://192.168.4.1 in your web browser")
                response = input("Continue anyway? (y/n): ")
                if response.lower() != "y":
                    sys.exit(1)
    return False


# Test ESP32 connection first
connected = test_esp32_connection()

# Load the YOLOv11 model
print("\nInitializing YOLO model...")
model = YOLO("yolo11n-pose.pt")
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {device}")
model.to(device)

# Initialize camera
print("\nInitializing camera...")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Keep track of last command time to avoid flooding
last_command_time = time.time()
COMMAND_INTERVAL = 1.0  # seconds between commands

print("\nStarting main loop. Press 'q' to quit.")
print("ESP32 command interval:", COMMAND_INTERVAL, "seconds")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Run YOLOv11 inference
    results = model(frame, device=device)

    # Get the annotated frame with pose detection
    annotated_frame = results[0].plot()

    # Try to send commands if enough time has passed
    current_time = time.time()
    if current_time - last_command_time >= COMMAND_INTERVAL:
        if len(results) > 0 and results[0].keypoints is not None:
            try:
                # Send a test angle to T1
                test_angle = 90
                response = requests.post(CONTROL_ENDPOINT, json={"servo": "T1", "angle": test_angle}, timeout=0.5)
                # Add connection status to frame (green if connected)
                status_text = f"ESP32: Connected (Last cmd: T1={test_angle})"
                cv2.putText(annotated_frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            except requests.exceptions.RequestException as e:
                # Add connection status to frame (red if not connected)
                cv2.putText(annotated_frame, f"ESP32: Not Connected ({str(e)[:30]}...)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        last_command_time = current_time

    # Display the frame
    cv2.imshow("YOLOv11 Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
