import yt_dlp
from datetime import datetime, timedelta
import os
import sys
import subprocess
import time
import re

def sanitize_url(url):
    """Clean the URL by removing non-printable characters and ANSI escape codes"""
    # Remove ANSI escape codes (e.g., \x1b[A, \x1b[B)
    url = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', url)
    # Remove other non-printable characters
    url = ''.join(c for c in url if c.isprintable())
    # Strip whitespace
    url = url.strip()
    return url

def validate_url(url):
    """Validate that the URL is a proper HTTP/HTTPS URL"""
    return url.startswith(('http://', 'https://'))

def find_ffmpeg():
    """Try multiple methods to find FFmpeg"""
    # 1. Check current directory
    if os.path.exists('ffmpeg.exe'):
        return os.path.abspath('ffmpeg.exe')
    
    # 2. Check PATH
    try:
        result = subprocess.run(['where', 'ffmpeg'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    # 3. Check common installation locations
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
    # Ensure download folder exists
    download_dir = "download"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Sanitize and validate the URL
    url = sanitize_url(url)
    if not validate_url(url):
        print(f"Error: '{url}' is not a valid HTTP/HTTPS URL. Please provide a valid URL starting with http:// or https://.")
        return

    ydl_opts = {
        'format': 'bestaudio/best' if format_choice == '2' else 'bestvideo+bestaudio/best',
        # Modify save path and filename format: save to download folder, filename as <title>.<ext>
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'extract_flat': 'in_playlist' if download_playlist else False,
        'playlistend': -1 if download_playlist else 1,  # Download all items in playlist
        'ignoreerrors': True,  # Ignore errors and continue with next video
        'verbose': True,  # More detailed output for debugging
    }

    ffmpeg_path = find_ffmpeg()
    if ffmpeg_path:
        print(f"Found FFmpeg: {ffmpeg_path}")
        ydl_opts['ffmpeg_location'] = ffmpeg_path
        if format_choice == '2':  # MP3
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
    else:
        print("Warning: FFmpeg not found. Will download in original format, unable to perform format conversion.")
        print("You can download FFmpeg from https://ffmpeg.org/download.html to enable format conversion.")

    # Strip the page number from the URL if present
    url = url.split('&p=')[0] if '&p=' in url else url

    for attempt in range(max_retries):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info and download_playlist:
                    urls = [entry.get('webpage_url', entry.get('url')) for entry in info['entries'] if entry]
                    ydl.download(urls)
                else:
                    ydl.download([url])
            print("Download completed successfully!")
            return
        except Exception as e:
            print(f"Download attempt {attempt + 1}/{max_retries} failed: {str(e)}")
            if attempt < max_retries - 1:
                print("Retrying after 5 seconds...")
                time.sleep(5)
            else:
                print("Maximum retry attempts reached, download failed.")
                print("Please check your network connection or try again later.")
                print("If the issue persists, consider updating yt-dlp:")
                print("pip install --upgrade yt-dlp")
                raise  # Re-raise the last exception for debugging

def main():
    video_url = input("Please enter the video URL to download: ")
    format_choice = input("Please choose download format (1: Video, 2: Audio): ")
    download_playlist = input("Download the entire playlist? (y/n): ").lower() == 'y'

    start_time = datetime.now()
    print(f"Download start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        download_media(video_url, format_choice, download_playlist)
    except Exception as e:
        print(f"Final error: {str(e)}")

    end_time = datetime.now()
    print(f"Download completion time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    duration = end_time - start_time
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    print(f"Media download completed! Total time: {hours} hours {minutes} minutes {seconds} seconds")

if __name__ == "__main__":
    main()
    # input("Press any key to exit...")