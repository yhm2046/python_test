import yt_dlp
from datetime import datetime, timedelta
import os
import sys
import subprocess

def find_ffmpeg():
    """嘗試多種方法找到 FFmpeg"""
    # 1. 檢查當前目錄
    if os.path.exists('ffmpeg.exe'):
        return os.path.abspath('ffmpeg.exe')
    
    # 2. 檢查 PATH
    try:
        result = subprocess.run(['where', 'ffmpeg'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    # 3. 檢查常見安裝位置
    common_paths = [
        r'C:\ffmpeg\bin\ffmpeg.exe',
        r'D:\ffmpeg\bin\ffmpeg.exe',
        os.path.expanduser('~\\Downloads\\ffmpeg\\bin\\ffmpeg.exe'),
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return None

# ... [前面的代码保持不变] ...

def download_media(url, format_choice, download_playlist=False):
    ydl_opts = {
        'format': 'bestaudio/best' if format_choice == '2' else 'bestvideo+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
    }

    if not download_playlist:
        ydl_opts['noplaylist'] = True

    ffmpeg_path = find_ffmpeg()
    if ffmpeg_path:
        print(f"找到 FFmpeg: {ffmpeg_path}")
        ydl_opts['ffmpeg_location'] = ffmpeg_path
        if format_choice == '2':  # MP3
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
    else:
        print("警告: 未找到 FFmpeg。將下載原始格式，無法進行格式轉換。")
        print("您可以從 https://ffmpeg.org/download.html 下載 FFmpeg 以啟用格式轉換功能。")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"下載過程中發生錯誤: {str(e)}")

# 使用示例
video_url = input("請輸入要下載的視頻URL: ")
format_choice = input("請選擇下載格式 (1: 視頻, 2: 音頻): ")
download_playlist = input("是否下載整個播放列表？(y/n): ").lower() == 'y'

start_time = datetime.now()
print(f"開始下載時間: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

download_media(video_url, format_choice, download_playlist)

# ... [后面的代码保持不变] ...

end_time = datetime.now()
print(f"下載完成時間: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

duration = end_time - start_time
hours, remainder = divmod(duration.seconds, 3600)
minutes, seconds = divmod(remainder, 60)

print(f"媒體下載完成！總耗時: {hours}小時 {minutes}分鐘 {seconds}秒")

input("按任意鍵退出...")