"""
YOLO Object Detection Module
Wrapper for YOLOv8 detection
"""

from ultralytics import YOLO
import cv2
import numpy as np


class YOLODetector:
    """
    YOLO object detection wrapper
    """
    
    def __init__(self, model_size='n'):  # 'n' for nano (fastest), 's', 'm', 'l', 'x'
        """
        Initialize YOLO detector
        
        Args:
            model_size: YOLOv8 model size ('n', 's', 'm', 'l', 'x')
        """
        self.model = YOLO(f'yolov8{model_size}.pt')
        
    def detect(self, frame, confidence=0.5):
        """
        Detect objects in frame
        
        Args:
            frame: Input frame (BGR image)
            confidence: Confidence threshold
            
        Returns:
            detections: List of detected objects with format:
                      [(class_name, confidence, x1, y1, x2, y2), ...]
        """
        results = self.model(frame, conf=confidence, verbose=False)
        
        detections = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = result.names[class_id]
                confidence = float(box.conf[0])
                
                # Get bounding box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                detections.append({
                    'class': class_name,
                    'confidence': confidence,
                    'box': (x1, y1, x2, y2)
                })
        
        return detections
    
    def draw_detections(self, frame, detections):
        """
        Draw detection boxes and labels on frame
        
        Args:
            frame: Input frame
            detections: List of detections from detect()
            
        Returns:
            annotated_frame: Frame with drawn detections
        """
        annotated = frame.copy()
        
        for det in detections:
            x1, y1, x2, y2 = det['box']
            class_name = det['class']
            confidence = det['confidence']
            
            # Draw bounding box
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw label
            label = f"{class_name} ({confidence:.2f})"
            cv2.putText(annotated, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return annotated
