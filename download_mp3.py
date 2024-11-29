import yt_dlp
from datetime import datetime

def download_and_convert_to_mp3(url):
    # 配置yt-dlp的选项
    ydl_opts = {
        'format': 'bestaudio/best',  # 选择最佳音频质量
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',  # 设置为320kbps，确保最高音质
        }],
        'outtmpl': '%(title)s.%(ext)s',  # 输出文件名模板
        'noplaylist': True,  # 如果只想下载单个视频，设置为True
    }

    # 开始下载
    start_time = datetime.now()
    print(f"开始下载时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"下载失败: {str(e)}")
        return

    # 结束下载
    end_time = datetime.now()
    print(f"运行结束于: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 计算耗时
    duration = end_time - start_time
    minutes, seconds = divmod(duration.seconds, 60)
    print(f"耗时: {minutes}分{seconds}秒")

def main():
    # 获取用户输入的YouTube视频URL
    url = input("请输入YouTube视频的URL: ")
    download_and_convert_to_mp3(url)

if __name__ == "__main__":
    main()
