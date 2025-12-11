"""
Demo Script - Two-Stage Video Recognition System
Shows example usage of the video processor without GUI
"""

import cv2
import os
from video_processor import VideoProcessor
from frame_difference import FrameDifferenceDetector
from yolo_detector import YOLODetector


def create_sample_video(output_path='sample_video.avi', duration_seconds=5, fps=30):
    """
    Create a sample video for testing
    Contains some frames with motion and some static frames
    """
    print(f"Creating sample video: {output_path}")
    
    # Video properties
    width, height = 640, 480
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Create 5 seconds of video
    total_frames = duration_seconds * fps
    
    for frame_num in range(total_frames):
        # Create frame
        frame = (255 * ((frame_num // 30) % 2)).astype('uint8')  # Alternate between black and white
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        
        # Add moving rectangle for some frames (motion)
        if frame_num % 60 < 30:  # Motion in first 30 frames of every 60
            x = (frame_num % 300) + 100
            cv2.rectangle(frame, (x, 100), (x + 100, 200), (0, 255, 0), -1)
        
        # Add frame number
        cv2.putText(frame, f"Frame: {frame_num}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        out.write(frame)
    
    out.release()
    print(f"✓ Sample video created: {output_path} ({total_frames} frames)")
    return output_path


def demo_frame_difference():
    """
    Demo 1: Test frame difference detection independently
    """
    print("\n" + "=" * 60)
    print("DEMO 1: Frame Difference Detection")
    print("=" * 60)
    
    # Create sample video
    video_path = create_sample_video('demo_sample.avi')
    
    detector = FrameDifferenceDetector(threshold=5000)
    cap = cv2.VideoCapture(video_path)
    
    frame_count = 0
    motion_frames = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        has_motion, diff, diff_count = detector.detect_difference(frame)
        
        if has_motion:
            motion_frames += 1
            status = "🔴 MOTION"
        else:
            status = "🟢 STATIC"
        
        frame_count += 1
        print(f"Frame {frame_count:3d}: {status} - Diff pixels: {diff_count:6d}")
    
    cap.release()
    
    print(f"\nResults:")
    print(f"  Total frames: {frame_count}")
    print(f"  Motion frames: {motion_frames}")
    print(f"  Static frames: {frame_count - motion_frames}")
    
    # Cleanup
    os.remove(video_path)


def demo_yolo_detection():
    """
    Demo 2: Test YOLO detection on a single frame
    """
    print("\n" + "=" * 60)
    print("DEMO 2: YOLO Object Detection")
    print("=" * 60)
    
    # Create sample video
    video_path = create_sample_video('demo_sample2.avi', duration_seconds=2)
    
    detector = YOLODetector(model_size='n')
    cap = cv2.VideoCapture(video_path)
    
    frame_num = 0
    total_detections = 0
    
    while frame_num < 10:  # Only process first 10 frames for demo
        ret, frame = cap.read()
        if not ret:
            break
        
        detections = detector.detect(frame, confidence=0.5)
        total_detections += len(detections)
        
        print(f"Frame {frame_num + 1}: {len(detections)} objects detected")
        for det in detections:
            print(f"  - {det['class']}: {det['confidence']:.2%} confidence")
        
        frame_num += 1
    
    cap.release()
    
    print(f"\nResults:")
    print(f"  Frames processed: {frame_num}")
    print(f"  Total detections: {total_detections}")
    
    # Cleanup
    os.remove(video_path)


def demo_two_stage_processing():
    """
    Demo 3: Full two-stage processing with speedup calculation
    """
    print("\n" + "=" * 60)
    print("DEMO 3: Two-Stage Processing with Speedup Calculation")
    print("=" * 60)
    
    # Create sample video
    video_path = create_sample_video('demo_sample3.avi', duration_seconds=3)
    
    processor = VideoProcessor(yolo_model_size='n')
    
    print("\nProcessing with Two-Stage Detection...")
    two_stage_result = processor.process_video_two_stage(video_path)
    
    print("\nProcessing with Full YOLO (baseline)...")
    full_yolo_result = processor.process_video_full_yolo(video_path)
    
    # Calculate speedup
    speedup_info = processor.calculate_speedup(two_stage_result, full_yolo_result)
    
    # Display results
    print("\n" + "=" * 60)
    print("RESULTS:")
    print("=" * 60)
    
    print(f"\nProcessing Time Comparison:")
    print(f"  Two-Stage:  {two_stage_result['total_time']:.2f} seconds")
    print(f"  Full YOLO:  {full_yolo_result['total_time']:.2f} seconds")
    print(f"  Time Saved: {speedup_info['time_saved']:.2f} seconds")
    
    print(f"\nSpeedup Metrics:")
    print(f"  Speedup Factor:    {speedup_info['speedup']:.2f}x")
    print(f"  Speedup Percent:   {speedup_info['speedup_percent']:.1f}%")
    
    print(f"\nDetection Statistics:")
    print(f"  Total Frames:      {two_stage_result['total_frames']}")
    print(f"  Motion Frames:     {two_stage_result['frames_with_detection']}")
    print(f"  YOLO Runs:         {two_stage_result['yolo_runs']}")
    print(f"  Frames Skipped:    {speedup_info['frames_skipped']}")
    print(f"  YOLO Reduction:    {speedup_info['yolo_reduction_percent']:.1f}%")
    
    print(f"\nEfficiency:")
    print(f"  ✓ Reduced YOLO runs by {speedup_info['yolo_reduction_percent']:.1f}%")
    print(f"  ✓ Achieved {speedup_info['speedup']:.2f}x speedup")
    print(f"  ✓ Saved {speedup_info['time_saved']:.2f} seconds")
    
    # Cleanup
    os.remove(video_path)


def main():
    """Run all demos"""
    print("""
╔════════════════════════════════════════════════════════╗
║  Two-Stage Video Recognition System - Demo Script     ║
╚════════════════════════════════════════════════════════╝
""")
    
    try:
        # Run demos
        demo_frame_difference()
        demo_yolo_detection()
        demo_two_stage_processing()
        
        print("\n" + "=" * 60)
        print("✅ All demos completed successfully!")
        print("=" * 60)
        print("\nNext Steps:")
        print("  Run the GUI application: python main_gui.py")
        print("  Upload your own video file for real-world testing")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {str(e)}")
        print("\nMake sure all dependencies are installed:")
        print("  pip install -r requirements.txt")


if __name__ == "__main__":
    main()
