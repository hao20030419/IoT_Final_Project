# Project Index & Navigation Guide

## 🎯 Start Here

**New to this project?** Start with:
1. Read **[README.md](README.md)** (5 min) - Overview and quick start
2. Run `python setup_check.py` (2 min) - Verify installation
3. Run `python main_gui.py` (immediate) - Launch application

---

## 📚 Documentation Files

### Core Documentation
- **[README.md](README.md)** - Main documentation
  - Quick start guide
  - Feature overview
  - Configuration options
  - Troubleshooting

- **[INSTALLATION.md](INSTALLATION.md)** - Setup instructions
  - Windows, macOS, Linux installation
  - GPU setup (CUDA/PyTorch)
  - Dependency installation
  - Common issues and fixes

- **[SPEEDUP_ANALYSIS.md](SPEEDUP_ANALYSIS.md)** - Performance details
  - Mathematical formulas
  - Real-world examples
  - Performance benchmarks
  - Algorithm explanations
  - Optimization strategies

### Quick References
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Command and configuration quick guide
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete project overview
- **[VISUAL_OVERVIEW.md](VISUAL_OVERVIEW.md)** - ASCII diagrams and visual explanations

---

## 💻 Application Files

### Main Application
- **[main_gui.py](main_gui.py)** - GUI application (380 lines)
  - Entry point: `python main_gui.py`
  - Tkinter-based interface
  - Video processing and playback
  - Metrics display

### Core Processing
- **[video_processor.py](video_processor.py)** - Main processing engine (200 lines)
  - Two-stage detection pipeline
  - Full YOLO baseline
  - Speedup calculation
  - Progress callbacks

- **[frame_difference.py](frame_difference.py)** - Motion detection (60 lines)
  - Grayscale conversion
  - Gaussian blur
  - Frame difference calculation
  - Change detection

- **[yolo_detector.py](yolo_detector.py)** - YOLOv8 wrapper (55 lines)
  - Model loading
  - Object detection
  - Bounding box extraction
  - Annotation drawing

### Configuration
- **[config.py](config.py)** - Configuration system (220 lines)
  - Parameter definitions
  - Preset profiles (fast, balanced, accurate, realtime)
  - Configuration manager class
  - Settings retrieval/modification

---

## 🛠️ Utility Files

### Tools
- **[setup_check.py](setup_check.py)** - Environment verification (150 lines)
  - Python version check
  - Dependency verification
  - GPU detection
  - System compatibility check
  - Run: `python setup_check.py`

- **[demo.py](demo.py)** - Example demonstrations (300 lines)
  - Sample video generation
  - Frame difference demo
  - YOLO detection demo
  - Two-stage processing demo
  - Run: `python demo.py`

### Dependencies
- **[requirements.txt](requirements.txt)** - Python packages
  - OpenCV
  - YOLOv8 (Ultralytics)
  - PyTorch
  - Pillow
  - NumPy
  - Installation: `pip install -r requirements.txt`

---

## 🗂️ Project Structure

```
IoT_Final_Project/
│
├── 📱 APPLICATION
│   ├── main_gui.py                   (GUI Application)
│   ├── video_processor.py            (Processing Engine)
│   ├── frame_difference.py           (Motion Detection)
│   ├── yolo_detector.py              (Object Detection)
│   └── config.py                     (Configuration)
│
├── 🔧 UTILITIES
│   ├── setup_check.py                (Environment Check)
│   ├── demo.py                       (Demo Scripts)
│   └── requirements.txt              (Dependencies)
│
├── 📖 DOCUMENTATION
│   ├── README.md                     (Main Guide)
│   ├── INSTALLATION.md               (Setup Instructions)
│   ├── SPEEDUP_ANALYSIS.md           (Performance Analysis)
│   ├── PROJECT_SUMMARY.md            (Project Overview)
│   ├── QUICK_REFERENCE.md            (Quick Guide)
│   ├── VISUAL_OVERVIEW.md            (Visual Diagrams)
│   └── INDEX.md                      (This File)
│
├── 🔐 GIT
│   ├── .git/                         (Version Control)
│   └── .gitignore                    (Git Ignore Rules)
│
└── 📋 CONFIG
    └── .gitignore                    (Git Configuration)
```

---

## 🚀 Quick Navigation

### I want to...

**Run the application**
→ `python main_gui.py` then see [README.md](README.md)

**Understand the two-stage approach**
→ See [VISUAL_OVERVIEW.md](VISUAL_OVERVIEW.md) and [SPEEDUP_ANALYSIS.md](SPEEDUP_ANALYSIS.md)

**Check my system is compatible**
→ Run `python setup_check.py`

**Install from scratch**
→ Follow [INSTALLATION.md](INSTALLATION.md)

**Try a demo first**
→ Run `python demo.py`

**Understand performance metrics**
→ Read [SPEEDUP_ANALYSIS.md](SPEEDUP_ANALYSIS.md)

**Change settings**
→ Edit [config.py](config.py) or use `apply_preset()`

**Debug issues**
→ Check [INSTALLATION.md](INSTALLATION.md) troubleshooting section

**Understand the code**
→ Read comments in [video_processor.py](video_processor.py) and other files

**Find quick commands**
→ See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

## 📊 Feature Map

### Two-Stage Detection
- **Stage 1**: [frame_difference.py](frame_difference.py) - Motion detection (5ms)
- **Stage 2**: [yolo_detector.py](yolo_detector.py) - Object detection (100ms, only on motion)
- **Pipeline**: [video_processor.py](video_processor.py) - Orchestrates both stages
- **Result**: 2-8x speedup depending on motion content

### Performance Calculation
- **Location**: [video_processor.py](video_processor.py) - `calculate_speedup()` method
- **Comparison**: Two-stage vs Full YOLO automatically
- **Metrics**: Speedup factor, percentage, time saved, YOLO reduction
- **Display**: [main_gui.py](main_gui.py) - Metrics panel

### User Interface
- **Application**: [main_gui.py](main_gui.py)
- **Features**: Video upload, playback, motion indicator, object display
- **Controls**: Play/pause/seek, frame slider, status display
- **Dashboard**: Real-time metrics and statistics

---

## 🎓 Learning Path

### Beginner (Just want to use it)
1. [README.md](README.md) - Overview
2. [INSTALLATION.md](INSTALLATION.md) - Install it
3. Run `python main_gui.py` - Use it
4. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick tips

### Intermediate (Want to understand it)
1. [VISUAL_OVERVIEW.md](VISUAL_OVERVIEW.md) - See how it works
2. [SPEEDUP_ANALYSIS.md](SPEEDUP_ANALYSIS.md) - Understand performance
3. Review [config.py](config.py) - See configuration options
4. Run `python demo.py` - See examples

### Advanced (Want to modify it)
1. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Architecture overview
2. Read [video_processor.py](video_processor.py) - Processing logic
3. Read [frame_difference.py](frame_difference.py) - Motion detection
4. Read [yolo_detector.py](yolo_detector.py) - Object detection
5. Read [main_gui.py](main_gui.py) - GUI implementation

---

## 📋 File Purposes at a Glance

| File | Purpose | Lines | User? | Dev? |
|---|---|---|---|---|
| main_gui.py | GUI Application | 380 | ✅ | ✅ |
| video_processor.py | Processing Engine | 200 | ❌ | ✅ |
| frame_difference.py | Motion Detection | 60 | ❌ | ✅ |
| yolo_detector.py | Object Detection | 55 | ❌ | ✅ |
| config.py | Configuration | 220 | ✅ | ✅ |
| setup_check.py | System Check | 150 | ✅ | ❌ |
| demo.py | Examples | 300 | ✅ | ✅ |
| README.md | Main Guide | 500 | ✅ | ✅ |
| INSTALLATION.md | Setup Guide | 400 | ✅ | ❌ |
| SPEEDUP_ANALYSIS.md | Performance | 600 | ✅ | ✅ |
| QUICK_REFERENCE.md | Quick Guide | 300 | ✅ | ❌ |
| PROJECT_SUMMARY.md | Overview | 250 | ✅ | ✅ |
| VISUAL_OVERVIEW.md | Diagrams | 400 | ✅ | ✅ |
| requirements.txt | Dependencies | 10 | ✅ | ❌ |

---

## 🔗 Cross-References

### Motion Detection System
- Code: [frame_difference.py](frame_difference.py) (60 lines)
- Algorithm: [SPEEDUP_ANALYSIS.md](SPEEDUP_ANALYSIS.md) - "Stage 1: Frame Difference Detection"
- Visual: [VISUAL_OVERVIEW.md](VISUAL_OVERVIEW.md) - "PROCESSING PIPELINE"
- Configuration: [config.py](config.py) - `FRAME_DIFF_CONFIG`

### Object Detection System
- Code: [yolo_detector.py](yolo_detector.py) (55 lines)
- Algorithm: [SPEEDUP_ANALYSIS.md](SPEEDUP_ANALYSIS.md) - "Stage 2: YOLOv8 Object Detection"
- Visual: [VISUAL_OVERVIEW.md](VISUAL_OVERVIEW.md) - "SYSTEM ARCHITECTURE"
- Configuration: [config.py](config.py) - `YOLO_CONFIG`

### Speedup Calculation
- Code: [video_processor.py](video_processor.py) - `calculate_speedup()` method
- Mathematical: [SPEEDUP_ANALYSIS.md](SPEEDUP_ANALYSIS.md) - "Performance Metrics"
- Examples: [SPEEDUP_ANALYSIS.md](SPEEDUP_ANALYSIS.md) - "Real-World Examples"
- Visual: [VISUAL_OVERVIEW.md](VISUAL_OVERVIEW.md) - "SPEEDUP VISUALIZATION"

### GUI Application
- Code: [main_gui.py](main_gui.py) (380 lines)
- Guide: [README.md](README.md) - "Using the GUI"
- Reference: [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - "GUI Quick Start"
- Visual: [VISUAL_OVERVIEW.md](VISUAL_OVERVIEW.md) - "GUI LAYOUT"

---

## ⚙️ Configuration Guide

### Easy Configuration (Presets)
- File: [config.py](config.py)
- Documentation: [README.md](README.md) - "Configuration" section
- Quick Reference: [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - "Configuration Quick Guide"
- Options: fast, balanced, accurate, realtime

### Advanced Configuration
- File: [config.py](config.py) - Edit `*_CONFIG` dictionaries
- Documentation: [SPEEDUP_ANALYSIS.md](SPEEDUP_ANALYSIS.md) - "Optimization Strategies"
- Parameters: threshold, model size, confidence, blur kernel

---

## 🎯 Common Tasks

### Task: Upload and process a video
1. Run: `python main_gui.py`
2. Click "Upload Video"
3. Select video file
4. Click "Process Video"
5. Wait for completion
6. View metrics
7. Play to review

### Task: Check if system is ready
1. Run: `python setup_check.py`
2. Verify all ✓ marks

### Task: Try a demo
1. Run: `python demo.py`
2. Review console output
3. Check example code

### Task: Make system faster
1. Edit [config.py](config.py)
2. Apply `apply_preset('fast')`
3. Or lower `FRAME_DIFF_CONFIG['threshold']`

### Task: Make system more accurate
1. Edit [config.py](config.py)
2. Apply `apply_preset('accurate')`
3. Or increase YOLO model size

### Task: Troubleshoot errors
1. See [INSTALLATION.md](INSTALLATION.md) - Troubleshooting section
2. Run `python setup_check.py`
3. Check error message matches one in guide

---

## 📞 Help Resources

| Problem | Where to Look |
|---|---|
| Installation | [INSTALLATION.md](INSTALLATION.md) |
| How to use GUI | [README.md](README.md) - "Using the GUI" |
| Performance questions | [SPEEDUP_ANALYSIS.md](SPEEDUP_ANALYSIS.md) |
| Quick commands | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |
| Project overview | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |
| Visual explanations | [VISUAL_OVERVIEW.md](VISUAL_OVERVIEW.md) |
| Quick start | [README.md](README.md) - "Quick Start" |
| Configuration | [config.py](config.py) and [README.md](README.md) |
| Code understanding | Code comments in `.py` files |

---

## 📊 Statistics

- **Total Files**: 14
- **Total Lines of Code**: ~1,600
- **Total Documentation**: ~2,500 lines
- **Configuration Options**: 20+
- **Preset Profiles**: 4
- **Supported Video Formats**: 8+
- **Python Minimum Version**: 3.8
- **Supported Platforms**: 3 (Windows, macOS, Linux)

---

## 🎉 Next Steps

1. **Installation** → [INSTALLATION.md](INSTALLATION.md)
2. **First Run** → `python setup_check.py`
3. **Try Demo** → `python demo.py`
4. **Launch GUI** → `python main_gui.py`
5. **Read More** → [README.md](README.md)
6. **Customize** → [config.py](config.py)

---

**Version**: 1.0 | **Updated**: December 2024  
**All Documentation Indexed** | **Easy Navigation** | **Complete Project**

---

### File Last Updated
- This index reflects the complete project as of December 2024
- All files are production-ready
- All documentation is comprehensive
- All features are fully implemented
