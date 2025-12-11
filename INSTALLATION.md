# Installation Guide - Two-Stage Video Recognition System

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Windows Installation](#windows-installation)
3. [macOS Installation](#macos-installation)
4. [Linux Installation](#linux-installation)
5. [GPU Setup](#gpu-setup)
6. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 4GB
- **Disk Space**: 2GB (for models and dependencies)
- **Internet**: For downloading models on first run

### Recommended Requirements
- **Python**: 3.10 or 3.11
- **RAM**: 8GB or more
- **GPU**: NVIDIA GPU with CUDA support (for acceleration)
- **Disk Space**: 5GB

## Windows Installation

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"

Verify installation:
```cmd
python --version
```

### Step 2: Clone the Project

```cmd
# Navigate to your desired directory
cd c:\lab\Homework\IoT_Final_Project

# Verify git is initialized
git status
```

### Step 3: Create Virtual Environment

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

### Step 4: Install Dependencies

```cmd
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

This may take 5-15 minutes depending on your internet speed.

### Step 5: Verify Installation

```cmd
# Run setup check
python setup_check.py
```

Expected output:
```
✓ Python Version: 3.x.x
  Status: ✅ Compatible

✓ OpenCV            - Installed
✓ Pillow            - Installed
✓ NumPy             - Installed
✓ YOLOv8            - Installed
✓ PyTorch          - Installed
✓ TorchVision      - Installed
✓ Tkinter          - Installed
```

### Step 6: Run the Application

```cmd
python main_gui.py
```

---

## macOS Installation

### Step 1: Install Python

Using Homebrew (recommended):
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11
```

Verify:
```bash
python3 --version
```

### Step 2: Install Dependencies (macOS-specific)

macOS may need additional setup for some packages:

```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install system dependencies
brew install opencv
```

### Step 3: Clone and Setup

```bash
# Navigate to project
cd ~/IoT_Final_Project

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 4: Install Python Packages

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Verify

```bash
python3 setup_check.py
```

### Step 6: Run

```bash
python3 main_gui.py
```

---

## Linux Installation

### Ubuntu/Debian

#### Step 1: Install System Dependencies

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
sudo apt install libopencv-dev python3-opencv
sudo apt install tk python3-tk
```

#### Step 2: Setup Project

```bash
cd ~/IoT_Final_Project

python3.11 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Python Packages

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Verify

```bash
python3 setup_check.py
```

#### Step 5: Run

```bash
python3 main_gui.py
```

### Fedora/RHEL

```bash
sudo dnf install python3.11 python3.11-devel
sudo dnf install opencv python3-opencv
sudo dnf install tk python3-tkinter

python3.11 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

python3 main_gui.py
```

---

## GPU Setup

### NVIDIA GPU with CUDA (Optional but Recommended)

#### Check GPU Availability

```python
python -c "import torch; print(torch.cuda.is_available())"
```

If True, you have CUDA support.

#### Install CUDA Toolkit (if needed)

1. Download from [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit)
2. Select your OS and follow installation instructions
3. Verify installation:

```bash
# Windows
nvidia-smi

# macOS/Linux
nvidia-smi
```

#### Install GPU-Accelerated PyTorch

```bash
# Uninstall current version
pip uninstall torch torchvision torchaudio -y

# Install CUDA 11.8 version (Windows/Linux)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

#### Verify GPU Setup

```bash
python setup_check.py
```

Should show:
```
✓ GPU Detected: NVIDIA GeForce RTX 3080
  CUDA Version: 11.8
  Status: ✅ GPU acceleration available
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'tkinter'"

**Windows:**
```cmd
# Reinstall Python with tcl/tk option
# Or install tk separately
pip install tk
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install python3-tk
```

**macOS:**
```bash
brew install python-tk@3.11
```

### Issue: "ModuleNotFoundError: No module named 'cv2'"

```bash
pip install --upgrade opencv-python
```

### Issue: Permission Denied on Linux/macOS

```bash
# Make script executable
chmod +x setup_check.py
chmod +x demo.py
chmod +x main_gui.py

# Run with python explicitly
python3 setup_check.py
```

### Issue: Virtual Environment Not Activating

**Windows:**
```cmd
# Check if venv folder exists
dir venv

# Try manual activation
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### Issue: YOLOv8 Model Download Failing

The model (~100MB) downloads on first use. This requires internet connection.

```bash
# Try manual download
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

# Use proxy if needed
pip install -r requirements.txt --proxy [user:passwd@]proxy.server:port
```

### Issue: "CUDA out of memory"

```bash
# Use CPU mode
python3 -c "from config import YOLO_CONFIG; YOLO_CONFIG['device'] = 'cpu'"

# Or use smaller model
python3 -c "from config import YOLO_CONFIG; YOLO_CONFIG['model_size'] = 'n'"
```

### Issue: Slow Processing

1. **Check GPU usage:**
   ```bash
   nvidia-smi  # Windows/Linux
   ```

2. **Try faster preset:**
   ```python
   python -c "from config import apply_preset; apply_preset('fast')"
   ```

3. **Reduce video resolution** or use smaller YOLO model

### Issue: GUI Window Not Opening

**Windows/macOS:**
- Ensure you're not in WSL (Windows Subsystem for Linux) when trying to use GUI
- Use native Windows Python, not WSL Python

**Linux with SSH:**
- GUI won't work over SSH without X11 forwarding
- Use `ssh -X` for X11 forwarding

### Issue: "ImportError: No module named '_tkinter'"

**Ubuntu:**
```bash
sudo apt install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

---

## Quick Diagnostic

Run this to get complete system info:

```bash
python setup_check.py
```

This will show:
- ✅ Python version compatibility
- ✅ All installed packages
- ✅ GPU availability
- ✅ System requirements

---

## Getting Help

1. Check the **Troubleshooting** section above
2. Review **README.md** for detailed documentation
3. Check **requirements.txt** versions match
4. Run `python setup_check.py` to verify installation
5. Try the **demo.py** script for isolated testing

---

## Next Steps

After successful installation:

1. Run demo: `python demo.py`
2. Launch GUI: `python main_gui.py`
3. Upload a test video
4. Process and review results

---

**Last Updated**: December 2024
**Python Version**: 3.8+
**OS Support**: Windows, macOS, Linux
