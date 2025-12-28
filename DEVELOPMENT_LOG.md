# Development Log — IoT_Final_Project

日期範圍：開發期間至 2025-12-28
作者：楊庭豪、徐浩翔、唐政遠

---

## 一、專案概覽
本專案實作一套「兩階段影片偵測系統」：
- 第一階段：使用幀差（frame-difference）做快速篩選，只針對有變化的影格執行第二階段。
- 第二階段：採用 YOLOv8 （Ultralytics）進行物件偵測，取得偵測結果與 confidence。
- 附加功能：將偵測後的影片進行壓縮（僅保留 YOLO 偵測到的影格，且保證至少保留 1 FPS 的關鍵影格），UI 顯示壓縮統計並提供下載。

技術棧：Python 3.13、OpenCV、PyTorch、Ultralytics YOLOv8、Tkinter、Pillow、NumPy。

主要檔案：
- `main_gui.py` — GUI 與互動邏輯（上傳、處理、播放、壓縮、顯示統計）
- `video_processor.py` — 兩階段處理流程、壓縮邏輯與速度比較
- `yolo_detector.py` — 封裝 YOLOv8 偵測呼叫（model 載入/推論）
- `frame_difference.py` — 幀差運算與快速篩選
- 測試與說明檔（如 `test_compression.py`、多份說明文件）

---

## 二、關鍵開發里程碑（時間軸式摘要）
1. 專案啟動：建立模組化架構，分離偵測、處理與 GUI。
2. 實作兩階段流程：先完成 `frame_difference.py` 與 `yolo_detector.py`，再由 `video_processor.py` 串接兩者。
3. UI 開發：使用 `Tkinter` 實作 `main_gui.py`，包含上傳、進度顯示、播放控制、結果面板與壓縮按鈕。
4. 壓縮功能：新增 `compress_video_smart()`，保證至少保留 1 FPS 的 keyframes 並保留所有 YOLO 偵測到的影格。
5. 測試：撰寫並執行 `test_compression.py`，在合成影片上驗證壓縮行為與統計資料。
6. 迭代修正：處理 GUI 事件綁定與 race-condition 問題（例如 slider recursion、NameError、resize handler 缺失等），完成多次小修。
7. 使用者需求變動：回退自動調整播放視窗的改動（將 canvas 保持靜態），並更新 GUI 以維持右側結果面板寬度穩定。

---

## 三、主要功能詳述
- 兩階段偵測
  - 篩選邏輯：計算相鄰影格差異量，若超過閾值則標記為需跑 YOLO 的影格。
  - 結果：減少 YOLO 推論次數以節省計算資源與時間。

- 全 YOLO baseline
  - 對整段影片逐影格跑 YOLO 以供比較，並用於計算加速效果（speedup）。

- 壓縮演算法（`compress_video_smart`）
  - 保留條件：只保留 YOLO 偵測到物件的影格，另外每秒至少保留 1 個影格作為 keyframe（frame_interval = max(1, int(fps))）。
  - 實作：逐影格讀取來源影片、決定是否寫入輸出檔（OpenCV VideoWriter），並回傳統計資訊（原始影格、保留影格、檔案大小、路徑等）。

- GUI（`main_gui.py`）
  - 上方控制列：上傳、處理、停止、壓縮與進度條
  - 左側播放區：固定 canvas (預設 640×480)、播放/暫停和幀滑桿
  - 右側結果區：影格資訊、效能指標（含加速倍數與 YOLO 減少率）、壓縮資訊
  - 事件處理：背景執行緒處理影片運算並以 progress_callback 更新 UI，避免主執行緒阻塞

---

## 四、錯誤修正與開發教訓
- 修正項目：
  - slider 回呼導致 RecursionError：加入 `self.updating_slider` 標記避免循環觸發。
  - 屬性命名錯誤（如 `video_frame` vs `self.video_frame`）：統一以實例屬性管理 widget。
  - Resize handler 不一致導致 AttributeError：移除不必要的 resize 綁定並還原為固定播放視窗需求。
- 教訓：UI 事件需以穩健方式處理（debounce、檢查屬性存在），長時間或密集任務應放到背景執行緒。

---

## 五、測試與驗證
- `test_compression.py`（synthetic video）驗證重點：
  - 建立測試影片（例：300 frames, 30 fps, 640×480）
  - 執行 `compress_video_smart()`，檢查輸出影格數、輸出檔案實際包含的影格數與統計回傳值
  - 測試結果（範例）：保留 10 張影格（1 fps × 10s）、檔案大小從 ~0.51MB 降至 ~0.03MB（約 95% 減少）

---

## 六、檔案變更要點（摘要）
- `main_gui.py`
  - 新增/修改：播放控制位置、固定 canvas 行為、壓縮資訊面板、錯誤修正（slider guard）、移除自動 resize handler
- `video_processor.py`
  - 新增：`compress_video_smart()` 與統計回傳
- `yolo_detector.py`, `frame_difference.py`
  - 保持原先功能（YOLO 封裝、幀差偵測）並被 `video_processor` 呼叫
- 測試文件與說明：新增多份 README/文檔與 `test_compression.py`

---

## 七、如何重現與使用（快速指引）
- 啟動 GUI（Windows cmd）：
```bat
python main_gui.py
```
- 操作流程：
  1. 點 `Upload Video` 選擇影片
  2. 點 `Process Video` 執行兩階段偵測（進度會顯示於上方）
  3. 執行完成後可在右側查看效能指標與影格資訊
  4. 點 `Compress & Download` 儲存壓縮後影片與查看壓縮統計

---

## 八、後續建議（可選改善項）
- 增加 batch 處理介面以一次處理多個影片。
- 在壓縮階段加入更彈性的保留策略（例如保留偵測連續區段或最小化 I-frame 間距）。
- 將 UI 重構為更現代的框架（例如 Electron 或 web 前端）以改善跨平台顯示與互動。

---

## 九、紀錄結語
此紀錄綜合了功能需求、實作細節、錯誤修正過程與驗證結果，可直接用於報告的「開發歷程」章節。若需要，我可以把這份紀錄摘要成 PPT 或中文報告段落（200–400 字）以方便放入正式報告中。
