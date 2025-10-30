import requests
import xml.etree.ElementTree as ET

# 請替換為你的 Google Storage 網址
url = "https://storage.googleapis.com/arphantom_filter/"

response = requests.get(url)

if response.status_code == 200:
    # 解析 XML 並處理命名空間
    root = ET.fromstring(response.text)

    # 定義命名空間，根據實際 XML 結構調整
    namespaces = {'ns': 'http://doc.s3.amazonaws.com/2006-03-01'}

    # 查找所有 <Contents> 元素並列出其中的 <Key> 值
    for contents in root.findall('.//ns:Contents', namespaces):
        key = contents.find('ns:Key', namespaces).text
        print(key)
else:
    print(f"Request failed with status code {response.status_code}")

