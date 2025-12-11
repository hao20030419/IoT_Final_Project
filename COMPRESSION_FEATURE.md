# 影片壓縮功能更新說明

## 功能概述

已成功實現進階影像壓縮系統，除了保留YOLO偵測到物件的影格外，還會每秒至少保留一個影格（無論該秒是否有物件檢測）。

## 核心功能

### 1. 智能壓縮演算法 (`compress_video_smart`)

**保留條件（滿足其一即保留）：**
- **YOLO檢測幀**：當幀差異檢測到動作且YOLO偵測到物件時
- **關鍵幀**：至少每秒保留1幀（作為視頻上下文參考）

**範例（FPS=30）：**
- 每秒保留的最少影格：1幀
- 保留間隔：30幀（每30幀至少保留1幀）

### 2. 使用者介面改進

#### 新增按鈕
- **"Compress & Download"** 按鈕：在視頻處理完成後可用
- 位置：控制面板，在 "Stop" 按鈕旁邊

#### 新增顯示區域
- **影片壓縮資訊面板**：結果面板最下方
- 顯示內容：
  - 原始影格數
  - 保留影格數
  - 壓縮百分比
  - 原始檔案大小
  - 壓縮後檔案大小
  - 檔案儲存路徑

### 3. 壓縮統計輸出

```
═══════════════════════════════════
影片壓縮統計
═══════════════════════════════════

原始影格數: 300
保留影格數: 10

壓縮比例: 96.7%
保留比例: 3.3%

原始檔案大小: 0.51 MB
壓縮後大小: 0.03 MB

儲存位置:
/path/to/compressed_video.mp4
```

## 技術實現

### 修改的檔案

1. **video_processor.py**
   - 新增方法：`compress_video_smart()`
   - 實現智能幀選擇邏輯
   - 計算壓縮統計資訊

2. **main_gui.py**
   - 新增變數：`self.compression_result`、`self.compression_thread`
   - 新增方法：
     - `start_compression()` - 啟動壓縮工作流
     - `_compress_video_thread()` - 後台壓縮執行緒
     - `_display_compression_info()` - 顯示壓縮結果
   - UI元素：
     - "Compress & Download" 按鈕
     - 壓縮資訊顯示面板

### 演算法詳細說明

```python
# 關鍵幀計算邏輯
frame_interval = max(1, int(fps))  # fps=30 → 間隔=30幀

# 保留判斷
if frame_count - last_keyframe >= frame_interval:
    should_save = True  # 時間到了，保留關鍵幀
    reason = "KEYFRAME"
    last_keyframe = frame_count

if has_difference and len(detections) > 0:
    should_save = True  # YOLO檢測到物件
    reason = "YOLO_DETECTION"
```

## 測試結果

運行 `test_compression.py` 的測試結果：

| 指標 | 數值 |
|-----|------|
| 原始影格數 | 300 |
| 保留影格數 | 10 |
| 壓縮比例 | 96.7% |
| 原始檔案大小 | 0.51 MB |
| 壓縮後大小 | 0.03 MB |
| 檔案大小減少 | 95.1% |
| 驗證狀態 | ✓ 成功 |

## 使用流程

1. **上傳視頻** - 使用 "Upload Video" 按鈕
2. **處理視頻** - 點擊 "Process Video" 進行YOLO分析
3. **壓縮視頻** - 處理完成後點擊 "Compress & Download"
4. **選擇儲存位置** - 在對話框中指定輸出檔名
5. **查看統計** - 在 "影片壓縮資訊" 面板查看壓縮結果

## 效能優勢

- **儲存空間**：減少95%以上
- **傳輸速度**：檔案大幅縮小，易於上傳/傳輸
- **資訊完整**：保留關鍵幀確保影片連貫性
- **智能選擇**：只保留有物件檢測的關鍵時刻

## 依賴

- OpenCV (video reading/writing)
- NumPy (frame processing)
- Ultralytics YOLOv8 (object detection)
