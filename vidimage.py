import cv2
import os
import time
from datetime import datetime

# Settings
CAPTURE_INTERVAL = 5  # seconds between image captures
save_folder = r"Lot Images"
os.makedirs(save_folder, exist_ok=True)

# ------------------- CAMERA SELECTION -------------------
# Plan A: Use laptop's built-in or default USB webcam
cam = cv2.VideoCapture(0)

# Plan B: Use external USB webcam or wireless CCTV/IP camera (uncomment and replace with actual URL or IP)
# cam = cv2.VideoCapture("http://<ip_or_url>:<port>/video")  # e.g., "http://192.168.1.10:8080/video"
# --------------------------------------------------------

if not cam.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Video properties
frame_width = int(cam.get(3))
frame_height = int(cam.get(4))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 20.0

# Output video file with timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
video_filename = os.path.join(save_folder, f"lot_{timestamp}.avi")
video_out = cv2.VideoWriter(video_filename, fourcc, fps, (frame_width, frame_height))

# Time tracker for image capture
last_capture_time = time.time()

print(f"Recording video and capturing image every {CAPTURE_INTERVAL} seconds.")
print(f"Saving to: {save_folder}")
print("Press 'q' to stop.")

try:
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Save frame to video
        video_out.write(frame)

        # Show live preview
        cv2.imshow("Recording... (Press 'q' to stop)", frame)

        # Save image every CAPTURE_INTERVAL seconds
        current_time = time.time()
        if current_time - last_capture_time >= CAPTURE_INTERVAL:
            img_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            img_filename = os.path.join(save_folder, f"lot_{img_timestamp}.jpg")
            cv2.imwrite(img_filename, frame)
            print(f"Image captured: {img_filename}")
            last_capture_time = current_time

        # Press 'q' to stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Stopped by user.")
            break

except KeyboardInterrupt:
    print("\nStopped by keyboard interrupt.")

finally:
    cam.release()
    video_out.release()
    cv2.destroyAllWindows()
