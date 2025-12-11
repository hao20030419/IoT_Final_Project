"""
QUICK REFERENCE GUIDE
=====================
Two-Stage Video Recognition System
"""

# Quick Start

## Installation (2 minutes)
```
pip install -r requirements.txt
```

## Verify Setup (1 minute)
```
python setup_check.py
```

## Run Application (immediate)
```
python main_gui.py
```

## Try Demo (5 minutes)
```
python demo.py
```

---

# File Guide

## Application Files
- **main_gui.py**: Launch this to run the GUI application
- **video_processor.py**: Core video processing engine
- **frame_difference.py**: Motion detection algorithm
- **yolo_detector.py**: Object detection wrapper
- **config.py**: Configuration and presets

## Tool Files
- **setup_check.py**: Verify Python environment
- **demo.py**: Run examples and demonstrations

## Documentation Files
- **README.md**: Main documentation with all features
- **INSTALLATION.md**: Platform-specific setup guide
- **SPEEDUP_ANALYSIS.md**: Performance mathematics and examples
- **PROJECT_SUMMARY.md**: Complete project overview

## Configuration Files
- **requirements.txt**: Python package dependencies

---

# GUI Quick Start

## Step 1: Upload Video
Click "Upload Video" → Select video file → Click "Process Video"

## Step 2: Processing
- Two-stage detection runs (frame diff + YOLO)
- Full YOLO baseline runs
- Speedup metrics calculated
- Results displayed automatically

## Step 3: Review Results
- View speedup statistics in Metrics panel
- Play/pause/seek video with controls
- See motion detection status (Red/Green indicator)
- View detected objects with bounding boxes

## Step 4: Interpret Metrics
- **Speedup Factor**: How many times faster (e.g., 2.5x)
- **Time Saved**: Seconds reduced compared to full YOLO
- **YOLO Reduction**: % of YOLO operations skipped

---

# Performance Indicators

| Video Type | Expected Speedup |
|---|---|
| Surveillance/Static | 5-15x |
| Presentation/Screen | 2-3x |
| General Video | 1.5-2.5x |
| Action/High Motion | 1.3-1.5x |

---

# Troubleshooting Quick Links

| Issue | Solution |
|---|---|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| GPU Not Detected | `python setup_check.py` |
| Slow Processing | Use `apply_preset('fast')` |
| Video Won't Load | Check format (.mp4, .avi, .mov, .mkv) |

---

# Configuration Quick Guide

## Change Detection Sensitivity
```python
# In video_processor.py:
self.frame_diff_detector = FrameDifferenceDetector(threshold=3000)  # More sensitive
self.frame_diff_detector = FrameDifferenceDetector(threshold=7000)  # Less sensitive
```

## Change YOLO Model Speed
```python
# In video_processor.py:
self.yolo_detector = YOLODetector(model_size='n')  # Fastest (default)
self.yolo_detector = YOLODetector(model_size='s')  # Fast
self.yolo_detector = YOLODetector(model_size='m')  # Medium
```

## Use Performance Preset
```python
from config import apply_preset

apply_preset('fast')       # Fastest
apply_preset('balanced')   # Balanced (default)
apply_preset('accurate')   # Most accurate
apply_preset('realtime')   # Real-time optimized
```

---

# Key Features

✨ Two-Stage Detection
- Frame difference (5ms): Detect motion
- YOLO (100ms): Only on moving frames
- Result: 2-8x speedup

📊 Automatic Speedup Calculation
- Compares two-stage vs full YOLO
- Shows time saved and percentage
- Displays YOLO reduction %

🎨 Professional GUI
- Video upload and playback
- Motion detection status display
- Real-time metrics dashboard
- Frame-by-frame analysis

---

# Usage Examples

## Basic Usage
```python
from video_processor import VideoProcessor

processor = VideoProcessor()
result = processor.process_video_two_stage('video.mp4')
print(f"Motion frames: {result['frames_with_detection']}")
print(f"YOLO runs: {result['yolo_runs']}")
```

## Batch Processing
```python
import os
from video_processor import VideoProcessor

processor = VideoProcessor()
for video in os.listdir('videos'):
    if video.endswith('.mp4'):
        result = processor.process_video_two_stage(f'videos/{video}')
        print(f"{video}: {result['frames_with_detection']} motion frames")
```

## Custom Configuration
```python
from frame_difference import FrameDifferenceDetector
from yolo_detector import YOLODetector

detector = FrameDifferenceDetector(threshold=4000)
yolo = YOLODetector(model_size='s')
```

---

# System Requirements

**Minimum**
- Python 3.8+
- 4GB RAM
- 2GB disk space
- Windows/macOS/Linux

**Recommended**
- Python 3.10+
- 8GB+ RAM
- NVIDIA GPU (CUDA)
- 5GB disk space

---

# Performance Tips

1. **For Speed**: Use `apply_preset('fast')`
2. **For Accuracy**: Use `apply_preset('accurate')`
3. **For Balance**: Use `apply_preset('balanced')`
4. **For Real-time**: Use `apply_preset('realtime')`

### Low Motion Videos (< 30% change)
→ Expect 5-15x speedup
→ Great for surveillance, presentations

### High Motion Videos (> 70% change)
→ Expect 1.3-1.5x speedup
→ Better for action movies

---

# File Purposes

| File | Purpose | Lines |
|---|---|---|
| main_gui.py | GUI application | 380 |
| video_processor.py | Processing engine | 200 |
| frame_difference.py | Motion detection | 60 |
| yolo_detector.py | YOLO wrapper | 55 |
| config.py | Configuration | 220 |
| setup_check.py | Verification tool | 150 |
| demo.py | Examples | 300 |

---

# Important Links

- **GitHub**: Check .git/ for version control
- **Python Docs**: docs.python.org
- **YOLOv8 Docs**: docs.ultralytics.com
- **OpenCV Docs**: docs.opencv.org

---

# Commands Reference

```bash
# Installation
pip install -r requirements.txt

# Verification
python setup_check.py

# Demo
python demo.py

# Run GUI
python main_gui.py

# Update Dependencies
pip install --upgrade -r requirements.txt

# Check GPU
python -c "import torch; print(torch.cuda.is_available())"
```

---

# Supported Video Formats

✅ MP4, AVI, MOV, MKV, FLV, WMV, ASF, MPEG

---

# Speedup Formula

```
Speedup = Full YOLO Time / Two-Stage Time
Speedup % = (Full - Two-Stage) / Full × 100
Time Saved = Full Time - Two-Stage Time
YOLO Reduction % = (1 - YOLO Runs / Total Frames) × 100
```

---

# Output Metrics

| Metric | Meaning |
|---|---|
| Speedup Factor | How many times faster (2.5x = 2.5 times faster) |
| Speedup % | Percentage improvement (50% = 50% faster) |
| Time Saved | Absolute seconds reduced |
| YOLO Reduction % | Percent of YOLO operations skipped |

---

# Tips & Tricks

1. **Reduce Frame Threshold**: Lower number = more motion detection
2. **Smaller YOLO Model**: Faster but less accurate
3. **Lower Confidence**: More detections but more false positives
4. **GPU**: Dramatically speeds up YOLO (3-4x faster)
5. **Lower Resolution**: Speeds up both frame diff and YOLO

---

# Presets Comparison

| Preset | Threshold | Model | Confidence | Use Case |
|---|---|---|---|---|
| fast | 3000 | nano | 0.6 | Speed critical |
| balanced | 5000 | nano | 0.5 | General use |
| accurate | 7000 | small | 0.4 | Quality matters |
| realtime | 2000 | nano | 0.7 | Real-time |

---

**Version**: 1.0 | **Updated**: December 2024 | **Python**: 3.8+
