import subprocess
import os
import sys
import re
import time
from threading import Thread
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def display_progress(download_cmd):
    process = subprocess.Popen(download_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    last_progress = None
    for line in iter(process.stdout.readline, ''):
        match = re.search(r'(\d+\.\d+)%\s*of\s*(\d+\.\d+)(MiB|GiB)\s*at\s*(\d+\.\d+)(\w)/s\s*ETA\s*(\d+:\d+)', line)
        if match:
            progress, size, unit, speed, speed_unit, eta = match.groups()
            if last_progress != progress:
                logging.info(f"下载进度: {progress}% of {size}{unit}, 速度: {speed}{speed_unit}/s, ETA: {eta}")
                last_progress = progress
        else:
            print(line.strip())
    process.stdout.close()
    process.wait()

def download_and_merge_video():
    start_time = time.time()
    video_count = 0

    while True:
        url = input("请输入YouTube视频的URL (或按Enter退出): ")
        if not url:
            print("程序退出。")
            break

        try:
            # 清理下载记录
            if os.path.exists("archive.txt"):
                os.remove("archive.txt")

            # 清理可能已存在的临时文件
            for file in os.listdir():
                if (file.endswith(('.part', '.ytdl')) or 
                    (file.endswith(('.webm', '.mp4', '.mkv')) and not file.startswith('Titanic • My Heart Will Go On • Celine Dion [F2RnxZnubCM]'))) and not file.endswith('.py'):
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
                # 尝试从文件名中获取
                downloaded_files = [f for f in os.listdir() if f.endswith(('.webm', '.mp4', '.mkv'))]
                if downloaded_files:
                    video_title = os.path.splitext(downloaded_files[0])[0]
                else:
                    print("无法从yt-dlp输出中提取视频标题，也没有找到下载的文件。")
                    continue

            # 假设yt-dlp会创建一个文件，可能是合并后的视频文件
            merged_file = next((f for f in os.listdir() if f.startswith(video_title) and f.endswith(('.webm', '.mp4', '.mkv'))), None)

            if merged_file:
                # 提取原始文件扩展名并重命名
                original_extension = os.path.splitext(merged_file)[1]
                output_filename = f"{video_title}.mp4" if original_extension.lower() != '.mp4' else merged_file
                if original_extension.lower() != '.mp4':
                    os.rename(merged_file, output_filename)
                logging.info(f"\n视频已经成功下载并命名为 {output_filename}")
                video_count += 1  # 增加下载视频的计数

                # 删除下载记录文件和临时文件
                if os.path.exists("archive.txt"):
                    os.remove("archive.txt")
                logging.info("下载记录文件已清理。")
                
                # 清理所有可能的临时文件，但不删除目标文件
                for file in os.listdir():
                    if (file.endswith(('.part', '.ytdl')) or 
                        (file.endswith(('.webm', '.mp4', '.mkv')) and file != output_filename)) and not file.endswith('.py'):
                        os.remove(file)
                logging.info("临时文件已清理。")

                if input("是否继续下载其他视频？(Y/n): ").lower() == 'n':
                    break
            else:
                print("无法找到下载的视频文件。")
        except subprocess.CalledProcessError as e:
            print(f"yt-dlp命令执行错误:\n{e.output}")
        except OSError as e:
            print(f"操作系统错误: {e}")
        except Exception as e:
            print(f"发生了一个意外的错误: {e}")

    # 计算总共运行时间
    end_time = time.time()
    total_time = int(end_time - start_time)
    minutes, seconds = divmod(total_time, 60)
    logging.info(f"\n程序运行总共耗时 {minutes:02d}分{seconds:02d}秒,共下载了{video_count}个视频文件")

    # 程序结束时直接删除archive.txt文件
    if os.path.exists("archive.txt"):
        os.remove("archive.txt")

if __name__ == "__main__":
    download_and_merge_video()
