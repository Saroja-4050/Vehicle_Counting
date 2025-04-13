import cv2
import os
import time
from datetime import datetime

# Set the capture interval in seconds
CAPTURE_INTERVAL = 30  # you can change this to 30, 60, etc.

# Define your folder path for saving images
save_folder = r"Lot Images"

# Create the folder if it doesn't exist
os.makedirs(save_folder, exist_ok=True)

# ------------------- CAMERA SELECTION -------------------
# Plan A: Use laptop's built-in or default USB webcam
cam = cv2.VideoCapture(0)

# Plan B: Use external USB webcam or wireless CCTV/IP camera (uncomment and replace with actual URL or IP)
# cam = cv2.VideoCapture("http://<ip_or_url>:<port>/video")  # e.g., "http://192.168.1.10:8080/video"
# --------------------------------------------------------

if not cam.isOpened():
    print("Error: Cannot access the webcam.")
    exit()

print(f"Capturing images every {CAPTURE_INTERVAL} seconds...")
print(f"Images will be saved to: {save_folder}")
print("Press Ctrl + C to stop.")

try:
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Timestamped filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(save_folder, f"lot_{timestamp}.jpg")

        # Save the image
        cv2.imwrite(filename, frame)
        print(f"Saved: {filename}")

        # Wait for the next capture
        time.sleep(CAPTURE_INTERVAL)

except KeyboardInterrupt:
    print("\nCapture stopped by user.")

finally:
    cam.release()
    cv2.destroyAllWindows()
