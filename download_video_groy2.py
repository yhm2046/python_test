import subprocess
import os
import sys
import re
import time
from threading import Thread

def display_progress(download_cmd):
    process = subprocess.Popen(download_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in iter(process.stdout.readline, ''):
        print(line.strip())
    process.stdout.close()
    process.wait()

def download_and_merge_video():
    start_time = time.time()
    downloaded_files = []
    video_count = 0  # 记录下载的视频文件数量

    while True:
        url = input("请输入YouTube视频的URL (或按Enter退出): ")
        if not url:
            print("程序退出。")
            break

        try:
            # 清理下载记录
            if os.path.exists("archive.txt"):
                os.remove("archive.txt")

            # 清理可能已存在的临时文件，但不删除 *.py 文件
            for file in os.listdir():
                if file.startswith(os.path.basename(url.split('?')[0])) and not file.endswith('.py'):
                    os.remove(file)

            # 下载视频和音频流，获取详细输出
            download_cmd = f"yt-dlp -v -f bestvideo+bestaudio --no-playlist --download-archive archive.txt {url}"
            thread = Thread(target=display_progress, args=(download_cmd,))
            thread.start()

            # 等待下载完成
            thread.join()

            # 从yt-dlp的输出中提取视频标题
            result = subprocess.run(download_cmd, shell=True, capture_output=True, text=True)
            title_match = re.search(r'Destination: (.*?)\.', result.stdout, re.DOTALL)
            if title_match:
                video_title = title_match.group(1)
            else:
                # 如果无法直接提取标题，我们尝试从文件名中获取
                downloaded_files = [f for f in os.listdir() if f.endswith(('.webm', '.mp4', '.mkv', '.m4a'))]
                if downloaded_files:
                    video_title = os.path.splitext(downloaded_files[0])[0]
                else:
                    print("无法从yt-dlp输出中提取视频标题，也无法找到下载的文件。")
                    continue

            # 找到下载的文件
            downloaded_files.extend([f for f in os.listdir() if f.startswith(video_title)])

            # 假设yt-dlp会创建一个文件，可能是合并后的视频文件
            merged_file = next((f for f in downloaded_files if f.endswith(('.webm', '.mp4', '.mkv'))), None)

            if merged_file:
                # 提取原始文件扩展名并重命名
                original_extension = os.path.splitext(merged_file)[1]
                output_filename = f"{video_title}.mp4"
                os.rename(merged_file, output_filename)
                print(f"\n视频已经成功下载并重命名为 {output_filename}")

                # 删除下载记录文件
                if os.path.exists("archive.txt"):
                    os.remove("archive.txt")
                print("下载记录文件已清理。")
                video_count += 1  # 增加下载视频的计数

                if input("是否继续下载其他视频？(Y/n): ").lower() == 'n':
                    break
            else:
                print("无法找到下载的视频文件。")
        except subprocess.CalledProcessError as e:
            print(f"命令执行错误:\n{e.output}")
        except Exception as e:
            print(f"发生了一个意外的错误: {e}")

    # 计算总共运行时间
    end_time = time.time()
    total_time = int(end_time - start_time)
    minutes, seconds = divmod(total_time, 60)
    print(f"\n程序运行总共耗时 {minutes}分{seconds}秒,共下载了{video_count}个视频文件")

if __name__ == "__main__":
    download_and_merge_video()
