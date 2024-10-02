import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from datetime import datetime

def sanitize_filename(filename):
    # 替换不合法字符
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_images(soup, base_url, folder_name):
    # 创建文件夹以保存图片
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 要忽略的图片文件名列表
    ignore_images = [
        "3day_160_600",
        "06-150-02",
        "160_600",
        "sh_2ntblogheadbar_logo",
        "icon.php",  # 忽略包含“icon.php”的文件
        "IMG_0040---.jpg",  # 忽略特定图片
        "product_lists.aspx"  # 忽略包含“product_lists.aspx”的文件
    ]

    # 查找所有图片标签
    img_tags = soup.find_all('img')
    for img in img_tags:
        img_url = img.get('src')
        if img_url:
            # 处理相对路径
            img_url = urljoin(base_url, img_url)
            img_name = os.path.basename(img_url)
            # 检查是否在忽略列表中
            if any(ignore in img_name for ignore in ignore_images):
                print(f"忽略图片: {img_name}")
                continue  # 跳过此图片

            try:
                img_data = requests.get(img_url).content
                img_name = sanitize_filename(img_name)  # 确保文件名合法
                img_path = os.path.join(folder_name, img_name)
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_data)
                print(f"下载图片: {img_path}")
            except Exception as e:
                print(f"无法下载图片 {img_url}: {e}")

def download_text(soup):
    # 提取网页中的所有文本
    text = soup.get_text(separator='\n', strip=True)
    
    # 忽略“返信”及其后面的内容
    if "返信" in text:
        text = text.split("返信")[0]
    
    return text

def extract_filename(title, text):
    # 提取标题中的目标部分
    if "裏女優に首ったけseason.2" in title:
        part = title.split("裏女優に首ったけseason.2")[1]
        # 提取“真白愛梨＝眞白愛梨＝園田ありさ＝あかね志帆”部分
        name_part = part.split('＝')[0:4]  # 取前四个等号前的部分
        base_name = sanitize_filename('＝'.join(name_part).strip())  # 返回拼接后的部分
        
        # 使用正则表达式检查文本中是否包含“は”后跟年份和日期
        match = re.search(r'は(\d{4})年(\d{1,2})月(\d{1,2})日生まれ', text)
        if match:
            year = match.group(1)  # 提取年份
            birth_date = f"{year}.{match.group(2).zfill(2)}.{match.group(3).zfill(2)}"  # 格式化为 YYYY.MM.DD
            current_year = datetime.now().year
            age = current_year - int(year)  # 计算年龄
            return sanitize_filename(f"{birth_date}-{age}y-{base_name}")  # 返回带有出生日期和年龄的文件名
        return base_name  # 返回原始文件名
    return "webpage"  # 默认文件名

def main(url):
    start_time = time.time()  # 记录开始时间
    # 获取网页内容
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 获取网页标题并提取文件名
        title = soup.title.string if soup.title else "webpage"
        print(f"提取的标题: {title}")  # 调试输出
        
        # 下载文本
        text_content = download_text(soup)
        file_name = extract_filename(title, text_content)  # 提取文件名
        
        # 创建文件夹以保存文本文件
        if not os.path.exists(file_name):
            os.makedirs(file_name)

        # 保存文本文件
        text_file_path = os.path.join(file_name, f'{file_name}.txt')
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text_content)
        print(f"网页文本已保存到 {file_name}文件夹下：{file_name}.txt")

        # 下载图片到以文件名命名的文件夹
        download_images(soup, url, file_name)
    else:
        print(f"无法访问网页，状态码: {response.status_code}")

    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算耗时
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"程序运行完成，总共耗时 {int(hours)}小时 {int(minutes)}分钟 {int(seconds)}秒")

if __name__ == "__main__":
    url = input("请输入要下载的网页 URL: ")
    main(url)