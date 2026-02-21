#!/usr/bin/env python3
"""
Capture a single frame from RTSP stream and save as image.
Usage: python capture_frame.py rtsp://url output.jpg
"""

import sys
import cv2

def capture_frame(rtsp_url, output_file):
    """Capture single frame from RTSP stream."""
    print(f"Connecting to: {rtsp_url}")
    
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("ERROR: Could not open RTSP stream")
        return False
    
    print("Connected, reading frame...")
    ret, frame = cap.read()
    
    if not ret:
        print("ERROR: Could not read frame")
        return False
    
    cv2.imwrite(output_file, frame)
    print(f"Frame saved to: {output_file}")
    
    cap.release()
    return True

# Default PiCamera RTSP URL
DEFAULT_RTSP = "rtsp://192.168.0.73:8554/cam"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python capture_frame.py [rtsp_url] <output.jpg>")
        print(f"Example: python capture_frame.py {DEFAULT_RTSP} cyd_screen.jpg")
        print(f"Default URL: {DEFAULT_RTSP}")
        sys.exit(1)
    
    # Handle both: capture_frame.py output.jpg  AND  capture_frame.py url output.jpg
    if len(sys.argv) == 2:
        # Single argument - use default URL, argument is output file
        rtsp_url = DEFAULT_RTSP
        output = sys.argv[1]
    else:
        # Two arguments - first is URL, second is output
        rtsp_url = sys.argv[1]
        output = sys.argv[2]
    
    print(f"Using RTSP URL: {rtsp_url}")
    success = capture_frame(rtsp_url, output)
    sys.exit(0 if success else 1)
