"""
SETUP GUIDE - Two-Stage Video Recognition System
==================================================

This script provides step-by-step setup instructions and validation.
Run this to verify your environment is properly configured.
"""

import sys
import subprocess
import platform

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"✓ Python Version: {version.major}.{version.minor}.{version.micro}")
    if version.major == 3 and version.minor >= 8:
        print("  Status: ✅ Compatible")
        return True
    else:
        print("  Status: ❌ Python 3.8+ required")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    packages = {
        'cv2': 'OpenCV',
        'PIL': 'Pillow',
        'numpy': 'NumPy',
        'ultralytics': 'YOLOv8',
        'torch': 'PyTorch',
        'torchvision': 'TorchVision',
        'tkinter': 'Tkinter'
    }
    
    all_installed = True
    print("\nDependency Check:")
    print("-" * 50)
    
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"✓ {name:20} - Installed")
        except ImportError:
            print(f"✗ {name:20} - NOT INSTALLED")
            all_installed = False
    
    return all_installed

def check_gpu():
    """Check if GPU is available"""
    try:
        import torch
        print("\nGPU Check:")
        print("-" * 50)
        if torch.cuda.is_available():
            print(f"✓ GPU Detected: {torch.cuda.get_device_name(0)}")
            print(f"  CUDA Version: {torch.version.cuda}")
            print("  Status: ✅ GPU acceleration available")
            return True
        else:
            print("✓ GPU: Not detected (CPU mode only)")
            print("  Status: ⚠️  Will use CPU (slower processing)")
            return False
    except Exception as e:
        print(f"GPU Check Error: {e}")
        return False

def print_requirements():
    """Print installation requirements"""
    print("\nInstallation Requirements:")
    print("=" * 50)
    
    os_type = platform.system()
    print(f"Operating System: {os_type}")
    print(f"Python Version: {sys.version}")
    
    print("\nRequired Packages:")
    print("  • opencv-python==4.8.1.78")
    print("  • ultralytics==8.0.212")
    print("  • torch==2.0.1")
    print("  • torchvision==0.15.2")
    print("  • Pillow==10.1.0")
    print("  • numpy==1.24.3")
    
    print("\nInstallation Command:")
    print("  pip install -r requirements.txt")

def print_quick_start():
    """Print quick start guide"""
    print("\nQuick Start Guide:")
    print("=" * 50)
    print("""
1. Install Dependencies:
   pip install -r requirements.txt

2. Run the Application:
   python main_gui.py

3. Upload Video:
   - Click "Upload Video"
   - Select a video file

4. Process Video:
   - Click "Process Video"
   - Wait for processing to complete

5. Review Results:
   - See speedup metrics
   - Play processed video
   - View frame-by-frame detections
""")

def main():
    """Main validation function"""
    print("""
╔══════════════════════════════════════════════════════╗
║  Two-Stage Video Recognition System - Setup Check   ║
╚══════════════════════════════════════════════════════╝
""")
    
    print("\nSystem Check:")
    print("=" * 50)
    python_ok = check_python_version()
    
    deps_ok = check_dependencies()
    check_gpu()
    
    print_requirements()
    
    if deps_ok and python_ok:
        print("\n✅ All checks passed! System is ready.")
        print_quick_start()
    else:
        print("\n❌ Some checks failed. Please install missing dependencies:")
        print("   pip install -r requirements.txt")
    
    print("\n" + "=" * 50)
    print("For detailed documentation, see README.md")
    print("=" * 50)

if __name__ == "__main__":
    main()
