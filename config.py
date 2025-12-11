"""
Configuration Module
Centralized configuration for all system parameters
"""

# Frame Difference Detection Parameters
FRAME_DIFF_CONFIG = {
    'threshold': 7000,          # Pixel count threshold to trigger detection
    'blur_kernel': (21, 21),    # Gaussian blur kernel size
    'diff_threshold': 30,       # Threshold for binary difference map
    'enabled': True             # Enable frame difference detection
}

# YOLO Detection Parameters
YOLO_CONFIG = {
    'model_size': 'n',          # Model size: 'n'=nano, 's'=small, 'm'=medium, 'l'=large, 'x'=xlarge
    'confidence': 0.5,          # Confidence threshold for detections
    'iou': 0.45,               # IoU threshold for NMS
    'device': '0',             # Device: '0' for GPU, 'cpu' for CPU
    'verbose': False           # Verbose output
}

# Video Processing Parameters
VIDEO_PROCESSING_CONFIG = {
    'max_frames': None,         # Maximum frames to process (None = all)
    'skip_frames': 0,          # Number of frames to skip at start
    'output_resolution': (640, 480),  # Output resolution for display
}

# GUI Parameters
GUI_CONFIG = {
    'window_width': 1400,
    'window_height': 900,
    'video_display_width': 640,
    'video_display_height': 480,
    'playback_fps': 30,
    'theme': 'default'
}

# Performance Monitoring
PERFORMANCE_CONFIG = {
    'collect_metrics': True,    # Collect detailed timing metrics
    'log_level': 'INFO',       # Logging level
    'save_results': False      # Save results to file
}

# Advanced Options
ADVANCED_CONFIG = {
    'use_gpu': True,           # Use GPU if available
    'adaptive_threshold': False, # Adaptive frame diff threshold
    'motion_tracking': False,  # Track motion across frames
    'save_output_video': False, # Save processed video
    'output_video_path': 'output.avi'
}


class Config:
    """Configuration manager"""
    
    @staticmethod
    def get_frame_diff_threshold():
        """Get frame difference threshold"""
        return FRAME_DIFF_CONFIG['threshold']
    
    @staticmethod
    def set_frame_diff_threshold(value):
        """Set frame difference threshold"""
        FRAME_DIFF_CONFIG['threshold'] = value
    
    @staticmethod
    def get_yolo_model_size():
        """Get YOLO model size"""
        return YOLO_CONFIG['model_size']
    
    @staticmethod
    def set_yolo_model_size(size):
        """Set YOLO model size"""
        if size in ['n', 's', 'm', 'l', 'x']:
            YOLO_CONFIG['model_size'] = size
        else:
            raise ValueError(f"Invalid model size: {size}")
    
    @staticmethod
    def get_confidence_threshold():
        """Get confidence threshold"""
        return YOLO_CONFIG['confidence']
    
    @staticmethod
    def set_confidence_threshold(value):
        """Set confidence threshold"""
        if 0 <= value <= 1:
            YOLO_CONFIG['confidence'] = value
        else:
            raise ValueError(f"Confidence must be between 0 and 1")
    
    @staticmethod
    def get_all_config():
        """Get all configuration"""
        return {
            'frame_diff': FRAME_DIFF_CONFIG,
            'yolo': YOLO_CONFIG,
            'video_processing': VIDEO_PROCESSING_CONFIG,
            'gui': GUI_CONFIG,
            'performance': PERFORMANCE_CONFIG,
            'advanced': ADVANCED_CONFIG
        }


# Preset configurations for different use cases
PRESETS = {
    'fast': {
        'description': 'Fastest processing (lowest accuracy)',
        'frame_diff_threshold': 3000,
        'yolo_model_size': 'n',
        'yolo_confidence': 0.6
    },
    'balanced': {
        'description': 'Balanced speed and accuracy',
        'frame_diff_threshold': 5000,
        'yolo_model_size': 'n',
        'yolo_confidence': 0.5
    },
    'accurate': {
        'description': 'Highest accuracy (slower processing)',
        'frame_diff_threshold': 7000,
        'yolo_model_size': 's',
        'yolo_confidence': 0.4
    },
    'realtime': {
        'description': 'Real-time processing optimization',
        'frame_diff_threshold': 2000,
        'yolo_model_size': 'n',
        'yolo_confidence': 0.7
    }
}


def apply_preset(preset_name):
    """Apply a preset configuration"""
    if preset_name not in PRESETS:
        raise ValueError(f"Unknown preset: {preset_name}")
    
    preset = PRESETS[preset_name]
    FRAME_DIFF_CONFIG['threshold'] = preset['frame_diff_threshold']
    YOLO_CONFIG['model_size'] = preset['yolo_model_size']
    YOLO_CONFIG['confidence'] = preset['yolo_confidence']
    
    print(f"✓ Applied preset: {preset_name} - {preset['description']}")


def get_preset_description(preset_name):
    """Get preset description"""
    if preset_name in PRESETS:
        return PRESETS[preset_name]['description']
    return "Unknown preset"


# Example usage
if __name__ == "__main__":
    print("Configuration Module")
    print("=" * 50)
    
    print("\nCurrent Configuration:")
    config = Config.get_all_config()
    for section, values in config.items():
        print(f"\n{section.upper()}:")
        for key, value in values.items():
            print(f"  {key}: {value}")
    
    print("\n\nAvailable Presets:")
    for name, preset in PRESETS.items():
        print(f"  {name}: {preset['description']}")
