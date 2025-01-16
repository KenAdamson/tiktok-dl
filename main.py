import yt_dlp
import os
import re
import json
import argparse
from typing import Optional, Dict, Any, List
from datetime import datetime


class TikTokDownloader:
    def __init__(self, save_path: str = 'tiktok_videos'):
        """Initialize TikTok downloader with configurable save path"""
        self.save_path = save_path
        self.create_save_directory()

    def create_save_directory(self) -> None:
        """Create the save directory if it doesn't exist"""
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate if the provided URL is a TikTok URL"""
        tiktok_pattern = r'https?://((?:vm|vt|www|video-[a-z0-9]+)\.)?(?:tiktok|tiktokv)\.(?:com|us)/.*'
        return bool(re.match(tiktok_pattern, url))

    def progress_hook(self, progress_callback):
        """Create a progress hook that calls back with progress info"""

        def hook(d: Dict[str, Any]) -> None:
            if d['status'] == 'downloading':
                # Convert _percent_str like ' 25.5%' to float 25.5
                percent = float(d.get('_percent_str', '0%').strip().replace('%', '') or 0)
                speed = d.get('_speed_str', 'N/A')
                eta = d.get('_eta_str', 'N/A')

                print(f"\rDownloading: {percent}% at {speed} ETA: {eta}", end='')
                if progress_callback:
                    progress_callback(percent)

            elif d['status'] == 'finished':
                print("\nDownload completed, finalizing...")
                if progress_callback:
                    progress_callback(100)

        return hook

    def get_filename(self, date_str: str) -> str:
        """Generate filename based on the date from metadata"""
        try:
            formatted_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%dT%H%M%S")
            return f"{formatted_date}.mp4"
        except ValueError:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"tiktok_{timestamp}.mp4"

    def download_video(self, video_url: str, date_str: str, progress_callback=None) -> Optional[str]:
        """Download a single TikTok video with progress updates"""
        if not self.validate_url(video_url):
            print(f"Error: Invalid TikTok URL - {video_url}")
            return None

        filename = self.get_filename(date_str)
        output_path = os.path.join(self.save_path, filename)

        ydl_opts = {
            'outtmpl': output_path,
            'format': 'best',
            'noplaylist': True,
            'quiet': False,
            'progress_hooks': [self.progress_hook(progress_callback)],
            'extractor_args': {'tiktok': {'webpage_download': True}},
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.tiktok.com/',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1'
            }
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                print(f"\nVideo successfully downloaded: {output_path}")
                return output_path

        except Exception as e:
            print(f"\nError downloading {video_url}: {str(e)}")

        return None


def get_favorites(data: Dict) -> List[Dict]:
    """Extract favorite videos from data"""
    return data.get("Activity", {}).get("Favorite Videos", {}).get("FavoriteVideoList", [])


def get_my_videos(data: Dict) -> List[Dict]:
    """Extract user's own videos from data"""
    return data.get("Video", {}).get("Videos", {}).get("VideoList", [])


def download_videos(downloader: TikTokDownloader, videos: List[Dict], progress_callback=None) -> None:
    """Download a list of videos with progress updates"""
    videos = [v for v in videos if v.get("Link") and v.get("Date")]
    total = len(videos)

    print(f"Found {total} videos to download")

    # Process downloads one at a time
    for i, video in enumerate(videos, 1):
        print(f"\nDownloading video {i} of {total}")
        if progress_callback:
            # Create a callback that updates both video and overall progress
            def video_progress(percent):
                progress_callback(i - 1, total, percent / 100, f"Downloading video {i} of {total}")

            downloader.download_video(video["Link"], video["Date"], video_progress)
        else:
            downloader.download_video(video["Link"], video["Date"])


def main(metadata_file: str, base_dir: str, video_type: str, progress_callback=None):
    # Determine target directory based on video type
    download_dir = os.path.join(base_dir, video_type)

    # Initialize downloader
    downloader = TikTokDownloader(save_path=download_dir)

    # Load metadata
    with open(metadata_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Get videos based on type
    if video_type == "favorites":
        videos = get_favorites(data)
    elif video_type == "my-videos":
        videos = get_my_videos(data)
    else:
        print(f"Unknown video type: {video_type}")
        return

    # Download the videos with progress updates
    download_videos(downloader, videos, progress_callback)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download videos from TikTok metadata.")
    parser.add_argument("metadata_file", help="Path to the metadata JSON file")
    parser.add_argument("download_dir", help="Base directory to save downloaded videos")
    parser.add_argument("--type", choices=["favorites", "my-videos"], default="favorites",
                        help="Type of videos to download (favorites or my-videos)")

    args = parser.parse_args()
    main(args.metadata_file, args.download_dir, args.type)