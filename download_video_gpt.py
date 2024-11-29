import yt_dlp
import time

def download_video(youtube_url, save_path="."):
    try:
        # 记录开始时间
        start_time = time.time()
        
        # yt-dlp 配置
        ydl_opts = {
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        
        # 记录结束时间
        end_time = time.time()
        
        # 计算总耗时
        elapsed_time = end_time - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        
        print(f"下载完成！总共耗时 {minutes} 分 {seconds} 秒")
    except Exception as e:
        print(f"下载出错: {e}")

# 输入 YouTube 视频 URL
url = input("请输入 YouTube 视频链接: ")

# 调用下载函数，默认保存路径为当前目录
download_video(url)
