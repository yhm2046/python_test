import yt_dlp
from datetime import datetime
import os
import subprocess
import time

def find_ffmpeg():
    """尝试多种方法找到 FFmpeg"""
    # 1. 检查当前目录
    if os.path.exists('ffmpeg.exe'):
        return os.path.abspath('ffmpeg.exe')
    
    # 2. 检查 PATH
    try:
        result = subprocess.run(['where', 'ffmpeg'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    # 3. 检查常见安装位置
    common_paths = [
        r'C:\ffmpeg\bin\ffmpeg.exe',
        r'D:\ffmpeg\bin\ffmpeg.exe',
        os.path.expanduser('~\\Downloads\\ffmpeg\\bin\\ffmpeg.exe'),
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return None

def download_media(url, format_choice, download_playlist=False, max_retries=3):
    ydl_opts = {
        'format': 'bestaudio/best' if format_choice == '2' else 'bestvideo+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'socket_timeout': 30,  # 增加超时时间
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
        print("警告: 未找到 FFmpeg。将下载原始格式，无法进行格式转换。")
        print("您可以从 https://ffmpeg.org/download.html 下载 FFmpeg 以启用格式转换功能。")

    for attempt in range(max_retries):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print("下载成功完成！")
            return
        except Exception as e:
            print(f"下载尝试 {attempt + 1}/{max_retries} 失败: {str(e)}")
            if attempt < max_retries - 1:
                print("等待 5 秒后重试...")
                time.sleep(5)
            else:
                print("达到最大重试次数，下载失败。")
                print("请检查您的网络连接，或稍后再试。")
                print("如果问题持续存在，请考虑更新 yt-dlp:")
                print("pip install --upgrade yt-dlp")

def main():
    video_url = input("请输入要下载的视频URL: ")
    format_choice = input("请选择下载格式 (1: 视频, 2: 音频): ")
    download_playlist = input("是否下载整个播放列表？(y/n): ").lower() == 'y'

    start_time = datetime.now()
    print(f"开始下载时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    download_media(video_url, format_choice, download_playlist)

    end_time = datetime.now()
    print(f"下载完成时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    duration = end_time - start_time
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    print(f"媒体下载完成！总耗时: {hours}小时 {minutes}分钟 {seconds}秒")

if __name__ == "__main__":
    main()
    input("按任意键退出...")