#!/usr/bin/env python3
"""
Experiment with different capture techniques for CYD screen reading.
Tries multiple approaches to find the clearest image.
"""

import cv2
import numpy as np
import sys

RTSP_URL = "rtsp://192.168.0.73:8554/cam"

def capture_basic():
    """Basic capture - just grab a frame."""
    cap = cv2.VideoCapture(RTSP_URL)
    if not cap.isOpened():
        return None
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None

def capture_multi_frame_average(num_frames=5):
    """Capture multiple frames and average them to reduce noise/blur."""
    cap = cv2.VideoCapture(RTSP_URL)
    if not cap.isOpened():
        return None
    
    frames = []
    for _ in range(num_frames):
        ret, frame = cap.read()
        if ret:
            frames.append(frame.astype(np.float32))
    cap.release()
    
    if not frames:
        return None
    
    # Average the frames
    averaged = np.mean(frames, axis=0).astype(np.uint8)
    return averaged

def capture_with_buffer():
    """Capture with buffer clearing - grab frames until stable."""
    cap = cv2.VideoCapture(RTSP_URL)
    if not cap.isOpened():
        return None
    
    # Read and discard first few frames (buffer clearing)
    for _ in range(10):
        cap.read()
    
    # Now capture the good frame
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None

def enhance_for_text_reading(frame):
    """Apply enhancements optimized for reading text on screens."""
    # Convert to LAB color space for better sharpening
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to L channel
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    
    # Merge back
    lab = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    # Sharpen
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)
    
    return sharpened

def reduce_blur_deconvolution(frame):
    """Try to reduce motion blur using deconvolution."""
    # Simple Wiener deconvolution approximation
    # Create a point spread function (PSF) assuming slight motion blur
    psf_size = 5
    psf = np.ones((psf_size, psf_size)) / (psf_size ** 2)
    
    # Apply to each channel
    result = np.zeros_like(frame, dtype=np.float32)
    for i in range(3):
        channel = frame[:, :, i].astype(np.float32)
        # Simple unsharp mask as approximation
        blurred = cv2.GaussianBlur(channel, (0, 0), 3)
        result[:, :, i] = cv2.addWeighted(channel, 1.5, blurred, -0.5, 0)
    
    return np.clip(result, 0, 255).astype(np.uint8)

def crop_to_cyd(frame):
    """Crop to just the CYD screen area."""
    # These coordinates are approximate - adjust based on actual position
    h, w = frame.shape[:2]
    # Crop center region where CYD is
    x1 = int(w * 0.35)
    y1 = int(h * 0.25)
    x2 = int(w * 0.75)
    y2 = int(h * 0.85)
    return frame[y1:y2, x1:x2]

def upscale_and_sharpen(frame, scale=2):
    """Upscale using Lanczos and then sharpen."""
    h, w = frame.shape[:2]
    upscaled = cv2.resize(frame, (w * scale, h * scale), interpolation=cv2.INTER_LANCZOS4)
    
    # Sharpen
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]])
    sharpened = cv2.filter2D(upscaled, -1, kernel)
    return sharpened

def main():
    print("=" * 60)
    print("CYD Screen Capture Experiments")
    print("=" * 60)
    
    # 1. Basic capture
    print("\n1. Capturing basic frame...")
    frame = capture_basic()
    if frame is not None:
        cv2.imwrite("exp_01_basic.jpg", frame)
        print("   Saved: exp_01_basic.jpg")
    
    # 2. Multi-frame average
    print("\n2. Capturing 5-frame average...")
    frame = capture_multi_frame_average(5)
    if frame is not None:
        cv2.imwrite("exp_02_average.jpg", frame)
        print("   Saved: exp_02_average.jpg")
    
    # 3. With buffer clearing
    print("\n3. Capturing with buffer clearing...")
    frame = capture_with_buffer()
    if frame is not None:
        cv2.imwrite("exp_03_buffered.jpg", frame)
        print("   Saved: exp_03_buffered.jpg")
    
    # 4. Text enhancement on best so far
    print("\n4. Applying text enhancement...")
    if frame is not None:
        enhanced = enhance_for_text_reading(frame)
        cv2.imwrite("exp_04_enhanced.jpg", enhanced)
        print("   Saved: exp_04_enhanced.jpg")
    
    # 5. Deconvolution
    print("\n5. Applying blur reduction...")
    if frame is not None:
        deblur = reduce_blur_deconvolution(frame)
        cv2.imwrite("exp_05_deblur.jpg", deblur)
        print("   Saved: exp_05_deblur.jpg")
    
    # 6. Crop to CYD
    print("\n6. Cropping to CYD area...")
    if frame is not None:
        cropped = crop_to_cyd(frame)
        cv2.imwrite("exp_06_cropped.jpg", cropped)
        print("   Saved: exp_06_cropped.jpg")
        
        # 7. Upscale the crop
        print("\n7. Upscaling crop 2x with sharpening...")
        upscaled = upscale_and_sharpen(cropped, 2)
        cv2.imwrite("exp_07_upscaled.jpg", upscaled)
        print("   Saved: exp_07_upscaled.jpg")
        
        # 8. Combined: crop + enhance + upscale
        print("\n8. Combined pipeline (crop + enhance + upscale)...")
        enhanced_crop = enhance_for_text_reading(cropped)
        final = upscale_and_sharpen(enhanced_crop, 2)
        cv2.imwrite("exp_08_final.jpg", final)
        print("   Saved: exp_08_final.jpg")
    
    print("\n" + "=" * 60)
    print("All experiments complete!")
    print("Review the images to see which is clearest for reading text.")
    print("=" * 60)

if __name__ == "__main__":
    main()
