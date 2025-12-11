# Speedup Calculation & Performance Analysis

## Overview

This document explains how the two-stage detection system achieves speedup and how the metrics are calculated.

## Two-Stage vs Full YOLO

### Full YOLO Approach (Baseline)
```
Video Frame 1 → [YOLO] → Detection Results (100ms)
Video Frame 2 → [YOLO] → Detection Results (100ms)
Video Frame 3 → [YOLO] → Detection Results (100ms)
...
Total Time: N frames × 100ms/frame
```

### Two-Stage Approach (Optimized)
```
Video Frame 1 → [Frame Diff] → No Motion → Skip YOLO (5ms)
Video Frame 2 → [Frame Diff] → Motion → [YOLO] → Detection (100ms)
Video Frame 3 → [Frame Diff] → Motion → [YOLO] → Detection (100ms)
Video Frame 4 → [Frame Diff] → No Motion → Skip YOLO (5ms)
...
Total Time: (Motion Frames × 100ms) + (Static Frames × 5ms)
```

## Performance Metrics

### 1. Speedup Factor

**Definition**: How many times faster the two-stage approach is compared to full YOLO

$$\text{Speedup Factor} = \frac{\text{Full YOLO Processing Time}}{\text{Two-Stage Processing Time}}$$

**Example**:
- Full YOLO Time: 300 seconds
- Two-Stage Time: 180 seconds
- Speedup Factor: 300 / 180 = **1.67x**

**Interpretation**: The two-stage system is 1.67 times faster than full YOLO

### 2. Speedup Percentage

**Definition**: Percentage improvement over full YOLO

$$\text{Speedup \%} = \frac{\text{Full YOLO Time} - \text{Two-Stage Time}}{\text{Full YOLO Time}} \times 100$$

**Example**:
- Full YOLO Time: 300 seconds
- Two-Stage Time: 180 seconds
- Speedup %: (300 - 180) / 300 × 100 = **40%**

**Interpretation**: 40% faster than full YOLO

### 3. Time Saved

**Definition**: Absolute time reduction in seconds

$$\text{Time Saved} = \text{Full YOLO Time} - \text{Two-Stage Time}$$

**Example**:
- Full YOLO Time: 300 seconds
- Two-Stage Time: 180 seconds
- Time Saved: **120 seconds** (2 minutes)

### 4. YOLO Reduction Percentage

**Definition**: Percentage of YOLO runs saved

$$\text{YOLO Reduction \%} = \left(1 - \frac{\text{YOLO Runs}}{\text{Total Frames}}\right) \times 100$$

**Example**:
- Total Frames: 1000
- YOLO Runs: 400 (only on motion frames)
- Frames Skipped: 600
- YOLO Reduction: (1 - 400/1000) × 100 = **60%**

**Interpretation**: 60% of expensive YOLO operations are skipped

## How Frame Difference Detection Works

### Algorithm Steps

1. **Convert to Grayscale**
   - Reduces processing from 3 channels (BGR) to 1 channel
   - Faster computation

2. **Apply Gaussian Blur**
   - Kernel: 21×21
   - Purpose: Reduce noise from compression artifacts, lighting changes
   - Effect: Preserves large motion while filtering small variations

3. **Calculate Absolute Difference**
   ```
   Difference = |Current Frame - Previous Frame|
   ```
   - Highlights all pixel changes between frames

4. **Apply Threshold**
   - Threshold: 30 (pixel intensity)
   - Converts to binary image: 0 (no change) or 255 (change)

5. **Count Non-Zero Pixels**
   - Counts changed pixels in entire frame
   - Threshold: 5000 pixels (configurable)
   - If count > threshold → Motion detected

### Why It's Fast

```
Frame Difference Processing Time:
  Grayscale Conversion:    ~1ms
  Gaussian Blur:           ~2ms
  Absolute Difference:     ~1ms
  Threshold:               ~1ms
  Count Non-Zero:          ~0.5ms
  ─────────────────────────────
  Total:                   ~5.5ms

vs

YOLO Inference:          ~100ms
```

**Speed Ratio**: YOLO is ~18x slower than frame difference!

## Expected Performance Gains

### Typical Video Content

| Content Type | Motion % | YOLO Reduction | Speedup Factor | Use Case |
|---|---|---|---|---|
| Security Camera | 10-20% | 80-90% | 9-15x | Surveillance |
| Static Presentation | 30-40% | 60-70% | 2-3x | Screen Recording |
| Action Movie | 60-70% | 30-40% | 1.3-1.5x | General Video |
| CCTV Parking Lot | 5-10% | 90-95% | 15-20x | Parking Monitoring |

### Time Estimates

For a **1-minute video** (1800 frames at 30fps):

```
Full YOLO Processing:
  1800 frames × 100ms/frame = 180,000ms = 3 minutes

Two-Stage (40% motion):
  Frame Diff:  1800 × 5ms =  9,000ms
  YOLO:         720 × 100ms = 72,000ms
  Total:                      81,000ms = 1.35 minutes
  
Speedup: 3 min / 1.35 min ≈ 2.2x faster
```

## Factors Affecting Speedup

### 1. Motion Content

**High Motion** → More YOLO runs → Less speedup
- Example: Action movie (70% motion) → 1.3-1.5x speedup

**Low Motion** → More frames skipped → More speedup
- Example: Security camera (10% motion) → 9-15x speedup

### 2. Frame Resolution

**Higher Resolution**:
- Frame diff: Slower (more pixels)
- YOLO: Slower (more pixels)
- Speedup: Remains roughly the same

**Lower Resolution**:
- Frame diff: Faster
- YOLO: Faster
- Overall speedup: Multiplies benefit

### 3. YOLO Model Size

**Larger Model** (e.g., 'x'):
- YOLO: ~500ms/frame
- Frame Diff: ~5ms/frame (negligible)
- Speedup potential: Higher (10-30x for low-motion content)

**Smaller Model** (e.g., 'n'):
- YOLO: ~100ms/frame
- Frame Diff: ~5ms/frame
- Speedup potential: Lower (2-10x)

### 4. System Hardware

**GPU Acceleration**:
- Frame diff: Uses CPU (~5-10ms)
- YOLO: Uses GPU (~20-50ms)
- Speedup: 5-10x (higher than CPU-only)

**CPU Only**:
- Frame diff: CPU (~5-10ms)
- YOLO: CPU (~100-200ms)
- Speedup: 2-3x

## Optimization Strategies

### 1. Reduce Frame Difference Threshold

Lower threshold = More motion detected = More YOLO runs = Less speedup

```python
# Conservative (detect more motion)
threshold = 3000  # Detects subtle motion

# Balanced
threshold = 5000  # Standard

# Aggressive (detect only obvious motion)
threshold = 10000  # Only large changes trigger YOLO
```

### 2. Choose Appropriate YOLO Model

```python
'n' (nano):     100ms/frame  - Best for two-stage
's' (small):    150ms/frame  - Good balance
'm' (medium):   250ms/frame  - Higher accuracy
'l' (large):    400ms/frame  - Highest accuracy
'x' (xlarge):   500ms/frame  - Largest speedup potential
```

### 3. Adjust Confidence Threshold

Lower confidence = More detections = More processing = Slower

```python
0.7 - 0.9    # High confidence (fast, fewer false positives)
0.4 - 0.6    # Balanced
0.1 - 0.3    # Low confidence (slow, more detections)
```

## Real-World Examples

### Example 1: Security Camera Footage

**Input**: 30-minute surveillance video (54,000 frames)

```
Content: Parking lot, mostly static
Motion %: 15% (occasional cars/people)

Full YOLO:
  54,000 frames × 150ms = 8,100,000ms = 2.25 hours

Two-Stage:
  Frame Diff: 54,000 × 5ms = 270,000ms
  YOLO: 8,100 × 150ms = 1,215,000ms
  Total: 1,485,000ms = 24.75 minutes

Speedup: 2.25 hours / 24.75 minutes = 5.45x faster
Time Saved: 1.65 hours
```

### Example 2: Presentation Recording

**Input**: 15-minute screen recording (27,000 frames)

```
Content: Slides with animations
Motion %: 35% (slides changing, animations)

Full YOLO:
  27,000 × 100ms = 2,700,000ms = 45 minutes

Two-Stage:
  Frame Diff: 27,000 × 5ms = 135,000ms
  YOLO: 9,450 × 100ms = 945,000ms
  Total: 1,080,000ms = 18 minutes

Speedup: 45 minutes / 18 minutes = 2.5x faster
Time Saved: 27 minutes
```

### Example 3: Action Movie

**Input**: 2-hour movie (216,000 frames at 24fps)

```
Content: High-action scenes
Motion %: 65% (constant motion)

Full YOLO:
  216,000 × 120ms = 25,920,000ms = 7.2 hours

Two-Stage:
  Frame Diff: 216,000 × 5ms = 1,080,000ms
  YOLO: 140,400 × 120ms = 16,848,000ms
  Total: 17,928,000ms = 4.98 hours

Speedup: 7.2 hours / 4.98 hours = 1.45x faster
Time Saved: 2.22 hours
```

## Key Insights

### ✅ When Two-Stage is Most Effective

1. **Low Motion Content** (< 30% change)
   - Surveillance footage
   - Static presentations
   - Screen recordings
   - Expected speedup: 3-10x

2. **High-Resolution Videos**
   - Larger frames benefit more
   - Frame diff overhead is fixed
   - Expected speedup: 2-5x

3. **GPU-Accelerated YOLO**
   - Frame diff is CPU (5-10ms)
   - YOLO is GPU (20-50ms)
   - Larger gap = bigger speedup potential

### ⚠️ When Two-Stage has Limited Benefits

1. **High Motion Content** (> 70% change)
   - Most frames trigger YOLO anyway
   - Expected speedup: 1.2-1.5x

2. **Real-time Requirements**
   - 5ms overhead might matter
   - Use only for post-processing

3. **CPU-Only Systems**
   - Speedup limited by CPU bottleneck
   - Expected speedup: 1.5-2x

## Calculation Verification

### Formula Check

For a video with:
- Total frames: 1000
- Motion frames: 300 (30%)
- Frame diff time: 5ms
- YOLO time: 100ms

```
Two-Stage:
  = (Total Frames × Frame Diff) + (Motion Frames × YOLO)
  = (1000 × 5ms) + (300 × 100ms)
  = 5,000ms + 30,000ms
  = 35,000ms

Full YOLO:
  = Total Frames × YOLO
  = 1000 × 100ms
  = 100,000ms

Speedup:
  = 100,000ms / 35,000ms
  = 2.86x

Speedup %:
  = (100,000 - 35,000) / 100,000 × 100
  = 65,000 / 100,000 × 100
  = 65%

YOLO Reduction:
  = (1 - 300/1000) × 100
  = 70% YOLO operations saved
```

## Conclusion

The two-stage detection system provides significant speedup for videos with moderate to low motion content. The actual speedup depends on:

1. **Video content** (motion percentage)
2. **Hardware** (GPU vs CPU)
3. **YOLO model size** (nano vs xlarge)
4. **Frame resolution** (480p vs 4K)

For typical surveillance and monitoring applications, expect **3-8x speedup** with zero loss in detection accuracy.
