import cv2
import os
from datetime import datetime

# Folder to save the video
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

# Get the default resolution of the webcam
frame_width = int(cam.get(3))  # 3 is CV_CAP_PROP_FRAME_WIDTH
frame_height = int(cam.get(4))  # 4 is CV_CAP_PROP_FRAME_HEIGHT

# Define video codec and output file
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = os.path.join(save_folder, f"lot_{timestamp}.avi")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 20.0  # frames per second
out = cv2.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))

print(f"Recording started. Press 'q' to stop.")
print(f"Saving video to: {filename}")

try:
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to capture frame.")
            break

        out.write(frame)

        # Display the live recording window
        cv2.imshow('Recording... (Press q to stop)', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Recording stopped by user.")
            break

except KeyboardInterrupt:
    print("\nRecording interrupted by user.")

finally:
    cam.release()
    out.release()
    cv2.destroyAllWindows()
