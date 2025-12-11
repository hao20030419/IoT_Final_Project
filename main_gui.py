"""
Main GUI Application
Two-stage image recognition system with UI interface
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import threading
import os
from video_processor import VideoProcessor
import time
from pathlib import Path


class VideoRecognitionApp:
    """
    GUI application for two-stage video recognition
    """
    
    def __init__(self, root):
        """Initialize the application"""
        self.root = root
        self.root.title("Two-Stage Video Recognition System")
        self.root.geometry("1400x900")
        
        self.video_processor = VideoProcessor(yolo_model_size='n')
        self.current_video_path = None
        self.processing_thread = None
        self.is_processing = False
        self.two_stage_result = None
        self.full_yolo_result = None
        self.current_frame_index = 0
        self.playback_thread = None
        self.is_playing = False
        self.updating_slider = False  # Flag to prevent circular callbacks
        self.compression_result = None  # Store compression results
        self.compression_thread = None  # Thread for compression
        # Video display properties (will be set on upload)
        self.video_width = 640
        self.video_height = 480
        self.video_fps = 30
        # Resize debounce handler id
        self._resize_after_id = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top control panel
        control_frame = ttk.LabelFrame(main_frame, text="Control Panel", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # File selection
        ttk.Button(control_frame, text="Upload Video", command=self.upload_video).pack(side=tk.LEFT, padx=5)
        self.video_label = ttk.Label(control_frame, text="No video selected", foreground="gray")
        self.video_label.pack(side=tk.LEFT, padx=5)
        
        # Processing buttons
        self.start_button = ttk.Button(control_frame, text="Process Video", command=self.start_processing, state=tk.DISABLED)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_processing, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Compression button
        self.compress_button = ttk.Button(control_frame, text="Compress & Download", command=self.start_compression, state=tk.DISABLED)
        self.compress_button.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        ttk.Label(control_frame, text="進度:").pack(side=tk.LEFT, padx=5)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, maximum=100, length=200)
        self.progress_bar.pack(side=tk.LEFT, padx=5)
        
        self.progress_label = ttk.Label(control_frame, text="0%")
        self.progress_label.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(control_frame, text="已就緒", foreground="blue")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Content frame
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left: Video display
        # Left: video frame (store as attribute)
        self.video_frame = ttk.LabelFrame(content_frame, text="影片播放", padding=10)
        self.video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.canvas = tk.Canvas(self.video_frame, bg='black', width=640, height=480)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Playback controls (kept in setup phase so they are always present)
        playback_control_frame = ttk.Frame(self.video_frame)
        playback_control_frame.pack(fill=tk.X, pady=(10, 0))

        self.play_button = ttk.Button(playback_control_frame, text="▶ 播放", command=self.play_video, state=tk.DISABLED)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = ttk.Button(playback_control_frame, text="⏸ 暫停", command=self.pause_video, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        ttk.Label(playback_control_frame, text="影格:").pack(side=tk.LEFT, padx=5)
        self.frame_var = tk.StringVar(value="0/0")
        self.frame_label = ttk.Label(playback_control_frame, textvariable=self.frame_var)
        self.frame_label.pack(side=tk.LEFT, padx=5)

        self.frame_scale = ttk.Scale(playback_control_frame, from_=0, to=0, orient=tk.HORIZONTAL,
                        command=self.on_frame_change)
        self.frame_scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

    
        
        # Right: Results panel (fixed min width to avoid being compressed)
        self.results_frame_min_width = 380
        self.results_frame = ttk.LabelFrame(content_frame, text="結果與效能指標", padding=10)
        # Pack with fill Y and a fixed width so it won't be compressed when canvas expands
        self.results_frame.pack(side=tk.RIGHT, fill=tk.Y)
        # Set a minimum width and disable geometry propagation so width stays
        try:
            self.results_frame.config(width=self.results_frame_min_width)
            self.results_frame.pack_propagate(False)
        except Exception:
            pass
        
        # Frame info
        info_frame = ttk.LabelFrame(self.results_frame, text="影格資訊", padding=5)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.frame_info_text = tk.Text(info_frame, height=8, width=40, state=tk.DISABLED)
        self.frame_info_text.pack(fill=tk.BOTH, expand=True)
        
        # Speedup metrics
        metrics_frame = ttk.LabelFrame(self.results_frame, text="效能指標", padding=5)
        metrics_frame.pack(fill=tk.BOTH, expand=True)
        
        self.metrics_text = tk.Text(metrics_frame, height=15, width=40, state=tk.DISABLED)
        self.metrics_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar for metrics
        scrollbar = ttk.Scrollbar(metrics_frame, orient=tk.VERTICAL, command=self.metrics_text.yview)
        self.metrics_text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Compression info frame
        compression_frame = ttk.LabelFrame(self.results_frame, text="影片壓縮資訊", padding=5)
        compression_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.compression_text = tk.Text(compression_frame, height=10, width=40, state=tk.DISABLED)
        self.compression_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar for compression info
        compression_scrollbar = ttk.Scrollbar(compression_frame, orient=tk.VERTICAL, command=self.compression_text.yview)
        self.compression_text.config(yscrollcommand=compression_scrollbar.set)
        compression_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def upload_video(self):
        """Handle video file upload"""
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv"), ("All files", "*.*")]
        )
        
        if file_path:
            self.current_video_path = file_path
            filename = os.path.basename(file_path)
            self.video_label.config(text=f"Loaded: {filename}", foreground="green")
            # Read video properties and resize display canvas to match video resolution
            try:
                cap = cv2.VideoCapture(file_path)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
                fps = cap.get(cv2.CAP_PROP_FPS) or 30
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
                cap.release()

                # Store properties but do NOT change canvas or window geometry
                # to keep the playback area static per user request.
                self.video_width = width
                self.video_height = height
                self.video_fps = fps

                # Keep canvas size unchanged; still reset slider display placeholders
                try:
                    self.frame_scale.config(to=0)
                    self.frame_var.set(f"0/0")
                except Exception:
                    pass

                self.start_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showwarning("Warning", f"Unable to read video properties: {e}")
                self.start_button.config(state=tk.NORMAL)
            
    def start_processing(self):
        """Start video processing in a separate thread"""
        if not self.current_video_path:
            messagebox.showerror("Error", "Please select a video first")
            return
        
        self.is_processing = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Processing: Two-Stage Detection...", foreground="orange")
        
        # Start processing in separate thread
        self.processing_thread = threading.Thread(target=self._process_video_thread)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        
    def _process_video_thread(self):
        """Background thread for video processing"""
        try:
            # Process with two-stage detection
            self.two_stage_result = self.video_processor.process_video_two_stage(
                self.current_video_path,
                progress_callback=self._update_progress
            )
            
            if not self.is_processing:
                return
            
            # Update status
            self.status_label.config(text="Processing: Full YOLO Baseline...", foreground="orange")
            
            # Process with full YOLO for comparison
            self.full_yolo_result = self.video_processor.process_video_full_yolo(
                self.current_video_path,
                progress_callback=self._update_progress
            )
            
            if not self.is_processing:
                return
            
            # Calculate speedup
            speedup_info = self.video_processor.calculate_speedup(self.two_stage_result, self.full_yolo_result)
            
            # Update UI
            self.root.after(0, self._display_results, speedup_info)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Processing error: {str(e)}"))
        finally:
            self.is_processing = False
            self.root.after(0, lambda: self.status_label.config(text="Ready", foreground="green"))
            self.root.after(0, lambda: self.stop_button.config(state=tk.DISABLED))
            
    def _update_progress(self, current, total):
        """Update progress bar"""
        progress = (current / total) * 100 if total > 0 else 0
        self.root.after(0, lambda: self._set_progress(progress, current, total))
        
    def _set_progress(self, progress, current, total):
        """Set progress bar value"""
        self.progress_var.set(progress)
        self.progress_label.config(text=f"{int(progress)}%")
        
    def _display_results(self, speedup_info):
        """Display processing results"""
        # Update metrics
        self.metrics_text.config(state=tk.NORMAL)
        self.metrics_text.delete(1.0, tk.END)
        
        metrics_text = f"""
═══════════════════════════════════
效能指標
═══════════════════════════════════

兩階段處理時間:
  {self.two_stage_result['total_time']:.2f} 秒

完整 YOLO 處理時間:
  {self.full_yolo_result['total_time']:.2f} 秒

加速結果:
───────────────────────────────────
加速倍數: {speedup_info['speedup']:.2f}x
節省時間: {speedup_info['time_saved']:.2f} 秒
加速百分比: {speedup_info['speedup_percent']:.1f}%

═══════════════════════════════════
檢測統計
═══════════════════════════════════

總影格數: {self.two_stage_result['total_frames']}
動作影格: {self.two_stage_result['frames_with_detection']}
YOLO 運算次數: {self.two_stage_result['yolo_runs']}
跳過的影格: {speedup_info['frames_skipped']}
YOLO 減少率: {speedup_info['yolo_reduction_percent']:.1f}%

═══════════════════════════════════
效率改進
───────────────────────────────────

使用兩階段檢測，你:
✓ 減少 YOLO 運算 {speedup_info['yolo_reduction_percent']:.1f}%
✓ 達到 {speedup_info['speedup']:.2f}x 加速
✓ 節省 {speedup_info['time_saved']:.2f} 秒
✓ 只處理有變化的影格
"""
        
        self.metrics_text.insert(1.0, metrics_text)
        self.metrics_text.config(state=tk.DISABLED)
        
        # Enable playback and compression
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.NORMAL)
        self.compress_button.config(state=tk.NORMAL)
        self.frame_scale.config(to=len(self.two_stage_result['frames']) - 1)
        self.frame_var.set(f"0/{len(self.two_stage_result['frames'])}")
        self.current_frame_index = 0
        
        # Display first frame
        self._display_frame(0)
        
        self.status_label.config(text="Complete! Ready to review results", foreground="green")
        
    def play_video(self):
        """Play the processed video"""
        if not self.two_stage_result:
            return
        
        self.is_playing = True
        self.play_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        
        self.playback_thread = threading.Thread(target=self._playback_thread)
        self.playback_thread.daemon = True
        self.playback_thread.start()
        
    def _playback_thread(self):
        """Background thread for video playback"""
        fps = self.two_stage_result['fps'] if self.two_stage_result['fps'] > 0 else 30
        frame_delay = 1.0 / fps
        
        while self.is_playing and self.current_frame_index < len(self.two_stage_result['frames']):
            start_time = time.time()
            
            self.root.after(0, self._display_frame, self.current_frame_index)
            self.current_frame_index += 1
            
            elapsed = time.time() - start_time
            sleep_time = max(0, frame_delay - elapsed)
            time.sleep(sleep_time)
        
        self.is_playing = False
        self.root.after(0, lambda: self.play_button.config(state=tk.NORMAL))
        
    def pause_video(self):
        """Pause video playback"""
        self.is_playing = False
        self.play_button.config(state=tk.NORMAL)
        
    def on_frame_change(self, value):
        """Handle frame slider change"""
        if self.updating_slider:
            return
        frame_index = int(float(value))
        self.current_frame_index = frame_index
        self._display_frame(frame_index)
        
    def _display_frame(self, frame_index):
        """Display a specific frame"""
        if not self.two_stage_result or frame_index >= len(self.two_stage_result['frames']):
            return
        
        frame = self.two_stage_result['frames'][frame_index]
        has_detection = self.two_stage_result['detected_frames'][frame_index]
        detections = self.two_stage_result['yolo_results'][frame_index]
        
        # Resize for display
        # Scale the frame to fit the canvas while preserving aspect ratio
        try:
            canvas_w = max(1, self.canvas.winfo_width())
            canvas_h = max(1, self.canvas.winfo_height())
            # Compute target size preserving video's aspect ratio
            vid_w = self.video_width or frame.shape[1]
            vid_h = self.video_height or frame.shape[0]
            vid_ar = vid_w / vid_h
            canvas_ar = canvas_w / canvas_h

            if canvas_ar > vid_ar:
                # canvas is wider relative to height -> limit by height
                target_h = canvas_h
                target_w = int(target_h * vid_ar)
            else:
                # canvas is taller relative to width -> limit by width
                target_w = canvas_w
                target_h = int(target_w / vid_ar)

            # Resize frame to target dimensions
            display_frame = cv2.resize(frame, (max(1, int(target_w)), max(1, int(target_h))))
        except Exception:
            display_frame = frame.copy()
        
        # Convert BGR to RGB and then to PhotoImage
        cv2_image = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv2_image)
        photo = ImageTk.PhotoImage(pil_image)
        
        self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.canvas.image = photo  # Keep a reference
        
        # Update frame info
        self.frame_info_text.config(state=tk.NORMAL)
        self.frame_info_text.delete(1.0, tk.END)
        
        info_text = f"""
影格: {frame_index + 1}/{len(self.two_stage_result['frames'])}

狀態: {"🔴 偵測到動作" if has_detection else "🟢 無動作"}

偵測到的物件: {len(detections)}

"""
        
        if detections:
            info_text += "偵測到的類別:\n"
            for det in detections:
                info_text += f"  • {det['class']}: {det['confidence']:.1%}\n"
        else:
            info_text += "(此影格未偵測到物件)"
        
        self.frame_info_text.insert(1.0, info_text)
        self.frame_info_text.config(state=tk.DISABLED)
        
        # Update frame label and scale (without triggering callback)
        self.frame_var.set(f"{frame_index + 1}/{len(self.two_stage_result['frames'])}")
        self.updating_slider = True
        self.frame_scale.set(frame_index)
        self.updating_slider = False
        
    def start_compression(self):
        """Start video compression"""
        if not self.two_stage_result:
            messagebox.showerror("Error", "Please process video first")
            return
        
        # Ask user for save location
        file_path = filedialog.asksaveasfilename(
            title="Save Compressed Video",
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        self.compress_button.config(state=tk.DISABLED)
        self.status_label.config(text="Compressing video...", foreground="orange")
        
        # Start compression in background thread
        self.compression_thread = threading.Thread(target=self._compress_video_thread, args=(file_path,))
        self.compression_thread.daemon = True
        self.compression_thread.start()
        
    def _compress_video_thread(self, output_path):
        """Background thread for video compression"""
        try:
            self.compression_result = self.video_processor.compress_video_smart(
                self.current_video_path,
                output_path,
                progress_callback=self._update_progress
            )
            
            # Update compression info display
            self.root.after(0, self._display_compression_info)
            
            self.status_label.config(text="Video compression complete!", foreground="green")
            messagebox.showinfo("Success", f"Video compressed successfully!\nSaved to: {output_path}")
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Compression error: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.compress_button.config(state=tk.NORMAL))
            
    def _display_compression_info(self):
        """Display compression statistics"""
        if not self.compression_result:
            return
        
        comp = self.compression_result
        
        compression_text = f"""
═══════════════════════════════════
影片壓縮統計
═══════════════════════════════════

原始影格數: {comp['original_frames']}
保留影格數: {comp['compressed_frames']}

壓縮比例: {comp['compression_percent']:.1f}%
保留比例: {(1 - comp['compression_ratio']) * 100:.1f}%

原始檔案大小: {comp['original_size_mb']:.2f} MB
壓縮後大小: {comp['compressed_size_mb']:.2f} MB

儲存位置:
{comp['output_path']}
"""
        
        self.compression_text.config(state=tk.NORMAL)
        self.compression_text.delete(1.0, tk.END)
        self.compression_text.insert(1.0, compression_text)
        self.compression_text.config(state=tk.DISABLED)
        
    def stop_processing(self):
        """Stop video processing"""
        self.is_processing = False
        self.is_playing = False
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = VideoRecognitionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
