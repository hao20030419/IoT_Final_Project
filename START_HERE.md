"""
STARTUP GUIDE
=============
Get your Two-Stage Video Recognition System up and running
in 3 simple steps!
"""

╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     TWO-STAGE VIDEO RECOGNITION SYSTEM                      ║
║     Startup Guide                                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝


STEP 1: INSTALL DEPENDENCIES (5 minutes)
═════════════════════════════════════════

💻 Windows:
───────────
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

💻 macOS/Linux:
─────────────
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


STEP 2: VERIFY INSTALLATION (2 minutes)
════════════════════════════════════════

Run the setup check:
  python setup_check.py

Expected output:
  ✓ Python Version: 3.x.x
    Status: ✅ Compatible
  
  ✓ OpenCV            - Installed
  ✓ Pillow            - Installed
  ✓ NumPy             - Installed
  ✓ YOLOv8            - Installed
  ✓ PyTorch          - Installed
  ✓ TorchVision      - Installed
  ✓ Tkinter          - Installed

⚠️  If you see red ✗ marks, go to INSTALLATION.md


STEP 3: RUN THE APPLICATION (immediate)
════════════════════════════════════════

Launch the GUI:
  python main_gui.py

A window will open with:
  ✓ "Upload Video" button
  ✓ "Process Video" button
  ✓ Video display area
  ✓ Metrics panel


═════════════════════════════════════════════════════════════

YOUR FIRST VIDEO (5 minutes)
════════════════════════════

1. Click "Upload Video"
   └─ Select a video file (.mp4, .avi, .mov, .mkv)

2. Click "Process Video"
   └─ System will process the video
   └─ Progress bar shows status
   └─ Takes 1-5 minutes depending on video length

3. View Results
   └─ Speedup metrics displayed
   └─ Video ready to play
   └─ Frame-by-frame information

4. Play Video
   └─ Click "Play" button
   └─ Use slider to seek
   └─ See motion detection status
   └─ View detected objects


═════════════════════════════════════════════════════════════

OPTIONAL: TRY THE DEMO (5 minutes)
═══════════════════════════════════

Want to see it in action without your own video?

  python demo.py

This will:
  ✓ Create sample videos
  ✓ Run frame difference detection
  ✓ Run YOLO detection
  ✓ Show speedup calculation
  ✓ Display all metrics


═════════════════════════════════════════════════════════════

NEED HELP?
═══════════

Installation issues?
  → Read INSTALLATION.md

How does it work?
  → Read README.md

Performance questions?
  → Read SPEEDUP_ANALYSIS.md

Quick commands?
  → Read QUICK_REFERENCE.md

Project overview?
  → Read PROJECT_SUMMARY.md

Navigation?
  → Read INDEX.md


═════════════════════════════════════════════════════════════

WHAT YOU GET
════════════

✨ Two-Stage Processing
  • Fast motion detection (5ms)
  • Smart object detection (100ms on motion only)
  • 2-8x speedup vs full YOLO

📊 Performance Metrics
  • Speedup factor (e.g., 2.5x)
  • Time saved (seconds)
  • YOLO reduction percentage
  • Detection statistics

🎨 Professional GUI
  • Video upload and playback
  • Real-time motion indicator
  • Object detection overlay
  • Comprehensive metrics dashboard


═════════════════════════════════════════════════════════════

QUICK REFERENCE
════════════════

Command                          What it does
────────────────────────────────────────────────────────────
python main_gui.py              Launch the GUI application
python setup_check.py           Verify installation
python demo.py                  Run examples
pip install -r requirements.txt Install dependencies


═════════════════════════════════════════════════════════════

EXPECTED SPEEDUP
═════════════════

Video Type           Motion   Expected Speedup
─────────────────────────────────────────────
Surveillance         10-20%   8-15x (Very fast!)
Presentation         30-40%   2.5-3.5x (Fast)
General Video        40-60%   1.8-2.5x (Good)
Action Movie         70-90%   1.2-1.5x (Okay)


═════════════════════════════════════════════════════════════

CONFIGURATION
══════════════

Want to adjust performance?

Edit config.py and use presets:

from config import apply_preset

apply_preset('fast')       # Fastest (3000 threshold)
apply_preset('balanced')   # Balanced (5000 threshold, default)
apply_preset('accurate')   # Most accurate (7000 threshold)
apply_preset('realtime')   # Real-time optimized (2000 threshold)


═════════════════════════════════════════════════════════════

SYSTEM REQUIREMENTS
════════════════════

Minimum                    Recommended
────────────────────────   ────────────────────────
Python 3.8+               Python 3.10+
4GB RAM                   8GB+ RAM
2GB disk space            5GB disk space
                          NVIDIA GPU (optional)


═════════════════════════════════════════════════════════════

TROUBLESHOOTING
════════════════

Problem: "ModuleNotFoundError"
Solution: pip install -r requirements.txt

Problem: GPU not detected
Solution: Run python setup_check.py to see status

Problem: Slow processing
Solution: Use apply_preset('fast') or smaller YOLO model

Problem: Video won't load
Solution: Try .mp4 format (most compatible)

More help?
→ See INSTALLATION.md Troubleshooting section


═════════════════════════════════════════════════════════════

MAIN FILES
═══════════

To Run                 File
──────────────────────────────────────────
GUI Application        main_gui.py
Setup Check            setup_check.py
Demo                   demo.py


═════════════════════════════════════════════════════════════

YOU'RE READY!
══════════════

✅ All files created
✅ Documentation ready
✅ Just run: python main_gui.py

Upload a video and experience 2-8x speedup!


═════════════════════════════════════════════════════════════

NEXT STEP: RUN THIS COMMAND
═══════════════════════════

  python main_gui.py

Then click "Upload Video" and select a video file.

That's it! The rest is easy.

═════════════════════════════════════════════════════════════

Need more info?
→ Check the README.md or other documentation files

Happy detecting! 🎉

═════════════════════════════════════════════════════════════
Version 1.0 | December 2024 | Python 3.8+ | All Platforms
═════════════════════════════════════════════════════════════
