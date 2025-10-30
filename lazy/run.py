# app.py
from flask import Flask, render_template
import requests
import xml.etree.ElementTree as ET
import sys
import os

# 將父目錄添加到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import BASE_URL

app = Flask(__name__)

# 從 Google Storage 取得 XML 資料並提取 Key 值
def fetch_image_keys():
    # 發送 GET 請求來獲取 XML 格式的內容
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        # 解析 XML 並處理命名空間
        root = ET.fromstring(response.text)
        # 定義命名空間，根據實際 XML 結構調整
        namespaces = {'ns': 'http://doc.s3.amazonaws.com/2006-03-01'}
        # 查找所有 <Contents> 元素並提取 <Key> 值
        keys = []
        for contents in root.findall('.//ns:Contents', namespaces):
            key = contents.find('ns:Key', namespaces).text
            keys.append(key)
        # 倒序排列 Key 值
        return list(reversed(keys))
    else:
        print(f"Request failed with status code {response.status_code}")
        return []

# 將圖片 URL 和生成的 Key 值傳遞到模板
@app.route('/')
def index():
    # 從 Google Storage 獲取 Key 值
    keys = fetch_image_keys()
    # 生成圖片 URL
    image_urls = [BASE_URL + key for key in keys]
    
    return render_template('index.html', image_urls=image_urls)

if __name__ == '__main__':
    app.run(debug=True)
