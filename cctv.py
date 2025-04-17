import cv2
import os
from datetime import datetime
import time

# Folder to save the video and images
save_folder = r"C:\Users\user1\Downloads\lot images"
os.makedirs(save_folder, exist_ok=True)

# Connect to USB CCTV camera (usually index 1 or 2)
cam = cv2.VideoCapture(1)  # Try 1, or change to 2 if needed

if not cam.isOpened():
    print("Error: Could not open USB camera. Try a different index.")
    exit()

# Get camera resolution
frame_width = int(cam.get(3))
frame_height = int(cam.get(4))

# Setup video writer
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
video_filename = os.path.join(save_folder, f"lot_{timestamp}.mp4")
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 20.0
out = cv2.VideoWriter(video_filename, fourcc, fps, (frame_width, frame_height))

print(f"Recording started. Press 'q' to stop.")
print(f"Saving video to: {video_filename}")

# Timing for image capture every 5 seconds
image_interval = 5  # seconds
last_image_time = time.time()

try:
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to capture frame.")
            break

        # Write video frame
        out.write(frame)

        # Show the frame
        cv2.imshow('Recording from CCTV... (Press q to stop)', frame)

        # Save image every 5 seconds
        current_time = time.time()
        if current_time - last_image_time >= image_interval:
            img_name = os.path.join(save_folder, f"image_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg")
            cv2.imwrite(img_name, frame)
            print(f"Image saved: {img_name}")
            last_image_time = current_time

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Recording stopped by user.")
            break

except KeyboardInterrupt:
    print("\nRecording interrupted by user.")

finally:
    cam.release()
    out.release()
    cv2.destroyAllWindows()
