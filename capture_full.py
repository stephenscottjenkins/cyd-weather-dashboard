#!/usr/bin/env python3
"""Capture full frame to verify crop region."""
import cv2

RTSP_URL = "rtsp://192.168.0.73:8554/cam"

# Updated crop settings
CROP_Y1, CROP_Y2 = 0.50, 0.98
CROP_X1, CROP_X2 = 0.36, 0.74

print("Capturing full frame...")
cap = cv2.VideoCapture(RTSP_URL)
for _ in range(5):
    cap.read()
ret, frame = cap.read()
cap.release()

if ret:
    h, w = frame.shape[:2]
    print(f"Full frame: {w}x{h}")
    cv2.imwrite("cyd_full_frame.jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
    
    # Draw crop region on copy
    overlay = frame.copy()
    y1, y2 = int(h * CROP_Y1), int(h * CROP_Y2)
    x1, x2 = int(w * CROP_X1), int(w * CROP_X2)
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 255, 0), 3)
    cv2.imwrite("cyd_with_crop_box.jpg", overlay, [cv2.IMWRITE_JPEG_QUALITY, 90])
    
    # Save just the crop
    cropped = frame[y1:y2, x1:x2]
    cv2.imwrite("cyd_crop_only.jpg", cropped, [cv2.IMWRITE_JPEG_QUALITY, 95])
    
    print(f"Crop region: ({x1},{y1}) to ({x2},{y2}) = {x2-x1}x{y2-y1}")
    print("Files saved.")
else:
    print("Failed to capture")
