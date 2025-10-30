# gcs-image-viewer 安裝與操作使用說明

**gcs-image-viewer** 是一款簡單的圖片展示工具，用於從 Google Cloud Storage 中提取圖片並展示在網頁上。該工具會自動解析存儲在雲端的圖片清單，並按倒序排列顯示圖片。專案提供了三種不同的前端顯示版本：標準版、水平滾動延遲載入版和垂直排列延遲載入版。

---

## 1. 功能特色

- **從雲端獲取圖片**：自動從指定的 Google Cloud Storage URL 獲取圖片列表。
- **多種顯示模式**：
  - **標準版**：一次性載入所有圖片，並在水平滾動容器中顯示。
  - **延遲載入版 (水平)**：當圖片滾動到可視區域時才載入，以提升初始頁面載入速度，採用水平佈局。
  - **延遲載入版 (垂直)**：與水平版類似，但每張圖片獨立成行，採用垂直佈局。
- **倒序排列**：預設將最新的圖片顯示在最前面。

---

## 2. 專案結構

```
.
├── config.py               # 設定檔，包含 Google Cloud Storage URL
├── lazy
│   ├── run.py              # 延遲載入版本的 Flask 應用程式
│   └── templates
│       ├── index.html      # 水平滾動的延遲載入模板
│       └── index2.html     # 垂直排列的延遲載入模板
├── templates
│   └── index.html          # 標準版的模板
├── README.md               # 本說明文件
├── requirements.txt        # Python 依賴套件
└── run.py                  # 標準版的 Flask 應用程式
```

---

## 3. 安裝與設定

### 3.1 環境準備

首先，你需要安裝 Python 3.6 以上版本，並確保 `pip`（Python 的包管理工具）已安裝。如果尚未安裝，請前往 [Python 官方網站](https://www.python.org/downloads/) 下載並安裝。

### 3.2 取得並安裝

1.  下載或複製此專案的程式碼到你的電腦上。
2.  開啟終端機，並進入專案目錄。
3.  執行以下命令安裝所有必要的 Python 套件：
    ```bash
    pip install -r requirements.txt
    ```

### 3.3 設定你的 Google Cloud Storage URL

這是最重要的步驟。開啟 `config.py` 檔案，並將 `BASE_URL` 的值修改為你自己的 Google Cloud Storage 儲存桶 URL。

```python
# config.py
# 將此 URL 替換為你的儲存桶公開存取 URL
BASE_URL = "https://storage.googleapis.com/your-bucket-name/"
```
**重要提示**：請確保你的 Google Cloud Storage 儲存桶已設定為公開存取，否則應用程式將無法讀取圖片列表。

---

## 4. 操作使用說明

你可以根據需求啟動不同版本的應用程式。

### 4.1 啟動標準版

此版本會一次性載入所有圖片。

在終端機中進入專案根目錄，並執行以下命令：

```bash
python run.py
```

### 4.2 啟動延遲載入版

此版本使用延遲載入技術，提升頁面效能。

在終端機中進入專案根目錄，並執行以下命令：

```bash
python lazy/run.py
```

伺服器啟動後，終端機中會顯示運行的地址，通常是：

```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

在你的瀏覽器中輸入該地址 (`http://127.0.0.1:5000/`)，即可訪問圖片展示頁面。

**注意**：`lazy/run.py` 預設載入 `index.html` (水平滾動版)。若要使用 `index2.html` (垂直排列版)，你需要手動修改 `lazy/run.py` 中的 `render_template` 函數：

```python
# 在 lazy/run.py 中
@app.route('/')
def index():
    # ...
    # 將 'index.html' 改為 'index2.html'
    return render_template('index2.html', image_urls=image_urls)
```

---

## 5. 常見問題

### 5.1 如何處理圖片不顯示的問題？

如果圖片未能顯示，請檢查以下項目：
1.  確保你的網路可以正常訪問 Google Cloud Storage。
2.  檢查 XML 檔案是否正確返回了 `<Key>` 值，並確保這些圖片文件是有效且公開可訪問的。
3.  使用瀏覽器的開發者工具檢查圖片 URL 是否正確。

### 5.2 如何更改圖片排序？

圖片目前是按倒序顯示的。如果希望改為正序顯示，只需在 `run.py` 或 `lazy/run.py` 中找到 `fetch_image_keys` 函數，並修改 `return` 語句：

```python
# 將
return list(reversed(keys))
# 改為
return keys
```

---

## 6. 其他建議

- **部署到伺服器**：如果要將此應用部署到線上伺服器，可以參考 [Flask 部署文檔](https://flask.palletsprojects.com/en/2.3.x/deploying/)。
- **自定義圖片路徑**：如果需要改變圖片 URL 的結構，只需修改 `config.py` 中的 `BASE_URL` 變數。
