import subprocess
import os
import sys
import re
import time
from threading import Thread
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def display_progress(download_cmd):
    process = subprocess.Popen(download_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    last_progress = None
    for line in iter(process.stdout.readline, ''):
        match = re.search(r'(\d+\.\d+)%\s*of\s*(\d+\.\d+)(MiB|GiB)\s*at\s*(\d+\.\d+)(\w)/s\s*ETA\s*(\d+:\d+)', line)
        if match:
            progress, size, unit, speed, speed_unit, eta = match.groups()
            if last_progress != progress:
                logging.info(f"Download progress: {progress}% of {size}{unit}, Speed: {speed}{speed_unit}/s, ETA: {eta}")
                last_progress = progress
        else:
            print(line.strip())
    process.stdout.close()
    process.wait()

def download_video_or_audio():
    start_time = time.time()
    video_count = 0

    while True:
        url = input("Please enter the YouTube video URL (or press Enter to exit): ")
        if not url:
            print("Program exiting.")
            break

        try:
            # Clear download record
            if os.path.exists("archive.txt"):
                os.remove("archive.txt")

            # Clear any existing temporary files
            for file in os.listdir():
                if (file.endswith(('.part', '.ytdl')) or 
                    (file.endswith(('.webm', '.mp4', '.mkv', '.mp3')) and not file.startswith('Titanic • My Heart Will Go On • Celine Dion [F2RnxZnubCM]'))) and not file.endswith('.py'):
                    os.remove(file)

            # Ask user if they want MP4 or MP3
            choice = input("Do you want to download MP4 (video) or MP3 (audio)? (1 for MP4, 2 for MP3): ")
            if choice == '1':
                download_cmd = f"yt-dlp -v -f bestvideo+bestaudio --no-playlist --download-archive archive.txt {url}"
                logging.info("Downloading as MP4.")
                file_extension = '.mp4'
            elif choice == '2':
                download_cmd = f"yt-dlp -v -f bestaudio --extract-audio --audio-format mp3 --no-playlist --download-archive archive.txt {url}"
                logging.info("Downloading as MP3.")
                file_extension = '.mp3'
            else:
                print("Invalid choice. Please choose '1' for MP4 or '2' for MP3.")
                continue

            thread = Thread(target=display_progress, args=(download_cmd,))
            thread.start()

            # Wait for download to complete
            thread.join()

            # Extract video title from yt-dlp output
            result = subprocess.run(download_cmd, shell=True, capture_output=True, text=True)
            title_match = re.search(r'Destination: (.*?)\.', result.stdout, re.DOTALL)
            if title_match:
                video_title = title_match.group(1)
            else:
                # Try to get from filename
                downloaded_files = [f for f in os.listdir() if f.endswith(file_extension)]
                if downloaded_files:
                    # Strip any extra identifiers like [BV1Te4y1M7fd] from the title
                    video_title = re.sub(r'\s*\[.*?\]', '', os.path.splitext(downloaded_files[0])[0])
                else:
                    print(f"Could not extract video title from yt-dlp output, nor find a downloaded {file_extension} file.")
                    continue

            # Assume yt-dlp creates the file with the correct extension
            merged_file = next((f for f in os.listdir() if f.startswith(video_title) and f.endswith(file_extension)), None)

            if merged_file:
                # Rename to match the format "xxx.mp4" or "xxx.mp3"
                new_filename = f"{video_title}{file_extension}"
                os.rename(merged_file, new_filename)
                logging.info(f"\nFile has been successfully downloaded and renamed to {new_filename}")
                video_count += 1  # Increment download count

                # Delete download record file and temporary files
                if os.path.exists("archive.txt"):
                    os.remove("archive.txt")
                logging.info("Download record file has been cleared.")
                
                # Clear all possible temporary files, but not the target file
                for file in os.listdir():
                    if (file.endswith(('.part', '.ytdl')) or 
                        (file.endswith(('.webm', '.mp4', '.mkv', '.mp3')) and file != new_filename)) and not file.endswith('.py'):
                        os.remove(file)
                logging.info("Temporary files have been cleared.")

                if input("Do you want to continue downloading other videos? (Y/n): ").lower() == 'n':
                    break
            else:
                print(f"Could not find the downloaded {file_extension} file.")
        except subprocess.CalledProcessError as e:
            print(f"yt-dlp command execution error:\n{e.output}")
        except OSError as e:
            print(f"OS error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    # Calculate total runtime
    end_time = time.time()
    total_time = int(end_time - start_time)
    minutes, seconds = divmod(total_time, 60)
    logging.info(f"\nProgram ran for a total of {minutes:02d} minutes {seconds:02d} seconds, downloaded {video_count} files")

    # Delete archive.txt file at program end
    if os.path.exists("archive.txt"):
        os.remove("archive.txt")

if __name__ == "__main__":
    download_video_or_audio()