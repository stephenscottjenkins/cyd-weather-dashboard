#!/usr/bin/env python3
"""
Optimized CYD screen capture for AI reading.
Best settings: Crop to screen + 2x upscale with light sharpening.
"""

import cv2
import numpy as np
import sys

RTSP_URL = "rtsp://192.168.0.73:8554/cam"

# Crop region for CYD screen (adjust these based on camera position)
# Format: (y_start, y_end, x_start, x_end) as ratios of image
CROP_Y1 = 0.50  # 50% from top - screen starts here
CROP_Y2 = 0.98  # 98% from top - screen ends near bottom
CROP_X1 = 0.36  # 36% from left - left edge of screen
CROP_X2 = 0.74  # 74% from left - right edge of screen

def capture_frame():
    """Capture frame from RTSP stream."""
    cap = cv2.VideoCapture(RTSP_URL)
    if not cap.isOpened():
        print("ERROR: Cannot connect to RTSP stream")
        return None
    
    # Discard first few frames (buffer clearing)
    for _ in range(5):
        cap.read()
    
    # Capture the good frame
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print("ERROR: Failed to capture frame")
        return None
    
    return frame

def process_for_reading(frame, upscale=2):
    """
    Process frame for optimal text reading:
    1. Crop to CYD screen area
    2. Upscale using Lanczos (best for text)
    3. Light sharpening
    """
    h, w = frame.shape[:2]
    
    # Crop to CYD screen
    y1, y2 = int(h * CROP_Y1), int(h * CROP_Y2)
    x1, x2 = int(w * CROP_X1), int(w * CROP_X2)
    cropped = frame[y1:y2, x1:x2]
    
    # Upscale using Lanczos (best quality for text)
    ch, cw = cropped.shape[:2]
    upscaled = cv2.resize(cropped, (cw * upscale, ch * upscale), 
                          interpolation=cv2.INTER_LANCZOS4)
    
    # Light sharpening (unsharp mask)
    blurred = cv2.GaussianBlur(upscaled, (0, 0), 2.0)
    sharpened = cv2.addWeighted(upscaled, 1.3, blurred, -0.3, 0)
    
    return sharpened

def main():
    output_file = sys.argv[1] if len(sys.argv) > 1 else "cyd_screen.jpg"
    upscale = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    
    print(f"Capturing from: {RTSP_URL}")
    print(f"Upscale: {upscale}x")
    
    frame = capture_frame()
    if frame is None:
        sys.exit(1)
    
    processed = process_for_reading(frame, upscale)
    cv2.imwrite(output_file, processed, [cv2.IMWRITE_JPEG_QUALITY, 95])
    
    print(f"Saved: {output_file}")
    print(f"Resolution: {processed.shape[1]}x{processed.shape[0]}")

if __name__ == "__main__":
    main()
