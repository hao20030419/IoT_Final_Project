"""
Frame Difference Detection Module
Detects scene changes between frames using frame differencing technique
"""

import cv2
import numpy as np


class FrameDifferenceDetector:
    """
    Detects motion/changes between frames using frame differencing
    """
    
    def __init__(self, threshold=5000, blur_kernel=(21, 21)):
        """
        Initialize the frame difference detector
        
        Args:
            threshold: Pixel count threshold to trigger motion detection
            blur_kernel: Kernel size for Gaussian blur
        """
        self.threshold = threshold
        self.blur_kernel = blur_kernel
        self.prev_frame = None
        
    def detect_difference(self, frame):
        """
        Detect if there is significant difference between current and previous frame
        
        Args:
            frame: Current frame (BGR image)
            
        Returns:
            (has_difference: bool, diff_image: ndarray, diff_count: int)
        """
        if self.prev_frame is None:
            self.prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return False, None, 0
        
        # Convert current frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        gray_blur = cv2.GaussianBlur(gray, self.blur_kernel, 0)
        prev_blur = cv2.GaussianBlur(self.prev_frame, self.blur_kernel, 0)
        
        # Calculate absolute difference
        diff = cv2.absdiff(gray_blur, prev_blur)
        
        # Apply threshold to get binary image
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
        
        # Count non-zero pixels (changed pixels)
        diff_count = cv2.countNonZero(thresh)
        
        # Determine if difference is significant
        has_difference = diff_count > self.threshold
        
        # Update previous frame
        self.prev_frame = gray.copy()
        
        return has_difference, diff, diff_count
    
    def reset(self):
        """Reset the detector state"""
        self.prev_frame = None
