"""
Video Processing Module
Handles two-stage detection and performance measurement
"""

import cv2
import time
import os
from frame_difference import FrameDifferenceDetector
from yolo_detector import YOLODetector


class VideoProcessor:
    """
    Two-stage video processing: frame difference detection + YOLO
    """
    
    def __init__(self, yolo_model_size='n'):
        """
        Initialize video processor
        
        Args:
            yolo_model_size: YOLOv8 model size
        """
        self.frame_diff_detector = FrameDifferenceDetector(threshold=5000)
        self.yolo_detector = YOLODetector(model_size=yolo_model_size)
        
    def process_video_two_stage(self, video_path, progress_callback=None):
        """
        Process video with two-stage detection (frame diff + YOLO)
        
        Args:
            video_path: Path to video file
            progress_callback: Callback function for progress updates
            
        Returns:
            dict with:
                - frames: List of processed frames
                - timestamps: Processing times per frame
                - detected_frames: Frames where difference was detected
                - yolo_results: YOLO detections per frame
                - total_time: Total processing time
                - frames_with_detection: Number of frames with difference detected
                - yolo_runs: Number of YOLO runs
        """
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        frames = []
        timestamps = []
        detected_frames = []
        yolo_results = []
        
        frame_count = 0
        frames_with_detection = 0
        yolo_runs = 0
        
        self.frame_diff_detector.reset()
        start_time = time.time()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_start = time.time()
            
            # Stage 1: Frame difference detection
            has_difference, _, diff_count = self.frame_diff_detector.detect_difference(frame)
            detected_frames.append(has_difference)
            
            detections = []
            
            # Stage 2: YOLO detection (only if difference detected)
            if has_difference:
                frames_with_detection += 1
                detections = self.yolo_detector.detect(frame)
                yolo_runs += 1
                annotated_frame = self.yolo_detector.draw_detections(frame, detections)
            else:
                annotated_frame = frame.copy()
            
            # Add status text
            status_text = "DETECTED: Difference" if has_difference else "No Difference"
            cv2.putText(annotated_frame, status_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if has_difference else (0, 0, 255), 2)
            
            frames.append(annotated_frame)
            yolo_results.append(detections)
            
            frame_time = time.time() - frame_start
            timestamps.append(frame_time)
            
            frame_count += 1
            
            if progress_callback:
                progress_callback(frame_count, total_frames)
        
        total_time = time.time() - start_time
        cap.release()
        
        return {
            'frames': frames,
            'timestamps': timestamps,
            'detected_frames': detected_frames,
            'yolo_results': yolo_results,
            'total_time': total_time,
            'frames_with_detection': frames_with_detection,
            'yolo_runs': yolo_runs,
            'total_frames': total_frames,
            'fps': fps
        }
    
    def process_video_full_yolo(self, video_path, progress_callback=None):
        """
        Process video with full YOLO detection (baseline for comparison)
        
        Args:
            video_path: Path to video file
            progress_callback: Callback function for progress updates
            
        Returns:
            dict with processing results
        """
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        frames = []
        timestamps = []
        yolo_results = []
        
        frame_count = 0
        start_time = time.time()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_start = time.time()
            
            # Run YOLO on every frame
            detections = self.yolo_detector.detect(frame)
            annotated_frame = self.yolo_detector.draw_detections(frame, detections)
            
            frames.append(annotated_frame)
            yolo_results.append(detections)
            
            frame_time = time.time() - frame_start
            timestamps.append(frame_time)
            
            frame_count += 1
            
            if progress_callback:
                progress_callback(frame_count, total_frames)
        
        total_time = time.time() - start_time
        cap.release()
        
        return {
            'frames': frames,
            'timestamps': timestamps,
            'yolo_results': yolo_results,
            'total_time': total_time,
            'total_frames': total_frames,
            'fps': fps
        }
    
    def calculate_speedup(self, two_stage_result, full_yolo_result):
        """
        Calculate speedup between two-stage and full YOLO
        
        Args:
            two_stage_result: Result dict from process_video_two_stage()
            full_yolo_result: Result dict from process_video_full_yolo()
            
        Returns:
            dict with speedup metrics
        """
        two_stage_time = two_stage_result['total_time']
        full_yolo_time = full_yolo_result['total_time']
        
        speedup = full_yolo_time / two_stage_time if two_stage_time > 0 else 0
        speedup_percent = ((full_yolo_time - two_stage_time) / full_yolo_time * 100) if full_yolo_time > 0 else 0
        
        time_saved = full_yolo_time - two_stage_time
        
        return {
            'speedup': speedup,
            'speedup_percent': speedup_percent,
            'time_saved': time_saved,
            'two_stage_time': two_stage_time,
            'full_yolo_time': full_yolo_time,
            'frames_skipped': full_yolo_result['total_frames'] - two_stage_result['yolo_runs'],
            'yolo_reduction_percent': (1 - two_stage_result['yolo_runs'] / full_yolo_result['total_frames']) * 100
        }

    def compress_video_smart(self, video_path, output_path, progress_callback=None):
        """
        Compress video by keeping only YOLO-detected frames + at least 1 frame per second
        
        Args:
            video_path: Path to input video file
            output_path: Path to output compressed video file
            progress_callback: Callback function for progress updates
            
        Returns:
            dict with compression statistics
        """
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Calculate frame interval for 1 frame per second
        # e.g., for fps=30, keep every 30 frames = 1 per second
        frame_interval = max(1, int(fps))
        
        # Setup video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frames_to_save = []
        frame_count = 0
        last_keyframe = -frame_interval  # Ensure first frame is saved as keyframe
        self.frame_diff_detector.reset()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Stage 1: Frame difference detection
            has_difference, _, _ = self.frame_diff_detector.detect_difference(frame)
            
            # Stage 2: Determine if frame should be saved
            should_save = False
            reason = ""
            
            # Check if it's time to save a keyframe (at least 1 per second)
            if frame_count - last_keyframe >= frame_interval:
                should_save = True
                reason = "KEYFRAME"
                last_keyframe = frame_count
            
            # If motion detected, run YOLO
            if has_difference:
                detections = self.yolo_detector.detect(frame)
                if len(detections) > 0:  # Only save if YOLO found objects
                    should_save = True
                    reason = "YOLO_DETECTION"
            
            if should_save:
                frames_to_save.append({
                    'frame': frame,
                    'frame_number': frame_count,
                    'reason': reason
                })
                out.write(frame)
            
            frame_count += 1
            
            if progress_callback:
                progress_callback(frame_count, total_frames)
        
        cap.release()
        out.release()
        
        compression_ratio = len(frames_to_save) / total_frames if total_frames > 0 else 0
        
        return {
            'output_path': output_path,
            'original_frames': total_frames,
            'compressed_frames': len(frames_to_save),
            'compression_ratio': compression_ratio,
            'compression_percent': (1 - compression_ratio) * 100,
            'original_size_mb': os.path.getsize(video_path) / (1024 * 1024) if os.path.exists(video_path) else 0,
            'compressed_size_mb': os.path.getsize(output_path) / (1024 * 1024) if os.path.exists(output_path) else 0,
            'fps': fps,
            'frames_to_save': frames_to_save
        }

