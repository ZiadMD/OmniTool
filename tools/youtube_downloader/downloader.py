"""
YouTube Downloader Core Module
Handles video/audio downloading using yt-dlp with progress tracking
"""

import os
from pathlib import Path
from typing import Callable, Dict, Optional
import yt_dlp


class YouTubeDownloader:
    """Core YouTube downloader class with progress tracking"""

    def __init__(self, download_directory: Optional[str] = None):
        """
        Initialize the YouTube downloader

        Args:
            download_directory: Directory to save downloads (defaults to ~/Downloads/YouTube)
        """
        if download_directory is None:
            home = Path.home()
            self.download_directory = str(home / "Downloads" / "YouTube")
        else:
            self.download_directory = download_directory

        os.makedirs(self.download_directory, exist_ok=True)
        self._progress_callback = None

    def set_progress_callback(self, callback: Callable[[Dict], None]):
        """Set a callback function to receive progress updates"""
        self._progress_callback = callback

    def _progress_hook(self, progress_data: Dict):
        """Internal progress hook for yt-dlp"""
        if progress_data['status'] == 'downloading':
            total_bytes = (progress_data.get('total_bytes') or
                          progress_data.get('total_bytes_estimate') or 0)
            downloaded_bytes = progress_data.get('downloaded_bytes', 0)
            speed = progress_data.get('speed', 0)
            eta = progress_data.get('eta', 0)

            percentage = (downloaded_bytes / total_bytes * 100) if total_bytes > 0 else 0
            speed_str = f"{self._format_bytes(speed)}/s" if speed else 'N/A'

            if self._progress_callback:
                self._progress_callback({
                    'status': 'downloading',
                    'percentage': percentage,
                    'downloaded': downloaded_bytes,
                    'total': total_bytes,
                    'speed': speed_str,
                    'eta': eta
                })

        elif progress_data['status'] == 'finished':
            if self._progress_callback:
                self._progress_callback({
                    'status': 'finished',
                    'filename': progress_data.get('filename', 'Unknown')
                })

    def _format_bytes(self, byte_size: float) -> str:
        """Format bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if byte_size < 1024.0:
                return f"{byte_size:.2f} {unit}"
            byte_size /= 1024.0
        return f"{byte_size:.2f} TB"

    def download_video(self, url: str, quality: str = 'best') -> Dict:
        """
        Download video in specified quality

        Args:
            url: YouTube video or playlist URL
            quality: Quality preference ('best', '2160p', '1440p', '1080p', '720p', '480p', '360p', '240p')

        Returns:
            dict: Download result with status and message
        """
        try:
            options = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': os.path.join(self.download_directory, '%(title)s.%(ext)s'),
                'progress_hooks': [self._progress_hook],
                'quiet': True,  # Changed to True to avoid yt-dlp output interfering
                'no_warnings': True,  # Changed to True
                'ignoreerrors': False,
                'merge_output_format': 'mp4',
                'nooverwrites': True,
                'noprogress': True,  # Disable yt-dlp's own progress bar
            }

            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)

                is_playlist = 'entries' in info
                video_count = len(list(info['entries'])) if is_playlist else 1

                ydl.download([url])

                return {
                    'status': 'success',
                    'message': f'Successfully downloaded {video_count} video(s)',
                    'is_playlist': is_playlist,
                    'count': video_count
                }

        except yt_dlp.utils.DownloadError as error:
            return {
                'status': 'error',
                'message': f'Download error: {str(error)}'
            }
        except Exception as error:
            return {
                'status': 'error',
                'message': f'Unexpected error: {str(error)}'
            }

    def download_audio(self, url: str) -> Dict:
        """
        Download audio only in MP3 format

        Args:
            url: YouTube video or playlist URL

        Returns:
            dict: Download result with status and message
        """
        try:
            options = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(self.download_directory, '%(title)s.%(ext)s'),
                'progress_hooks': [self._progress_hook],
                'quiet': True,  # Changed to True
                'no_warnings': True,  # Changed to True
                'ignoreerrors': False,
                'noprogress': True,  # Disable yt-dlp's own progress bar
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'nooverwrites': True,
            }

            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)

                is_playlist = 'entries' in info
                audio_count = len(list(info['entries'])) if is_playlist else 1

                ydl.download([url])

                return {
                    'status': 'success',
                    'message': f'Successfully downloaded {audio_count} audio file(s)',
                    'is_playlist': is_playlist,
                    'count': audio_count
                }

        except yt_dlp.utils.DownloadError as error:
            return {
                'status': 'error',
                'message': f'Download error: {str(error)}'
            }
        except Exception as error:
            return {
                'status': 'error',
                'message': f'Unexpected error: {str(error)}'
            }

    def get_video_info(self, url: str) -> Dict:
        """
        Get video information without downloading

        Args:
            url: YouTube video URL

        Returns:
            dict: Video information or error
        """
        try:
            options = {
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)

                if 'entries' in info:
                    # Playlist
                    return {
                        'status': 'success',
                        'type': 'playlist',
                        'title': info.get('title', 'Unknown Playlist'),
                        'count': len(list(info['entries'])),
                        'uploader': info.get('uploader', 'Unknown'),
                        'thumbnail': info.get('thumbnail', ''),
                        'description': info.get('description', '')
                    }
                else:
                    # Single video - return full info including formats
                    return {
                        'status': 'success',
                        'type': 'video',
                        'title': info.get('title', 'Unknown'),
                        'duration': info.get('duration', 0),
                        'uploader': info.get('uploader', 'Unknown'),
                        'view_count': info.get('view_count', 0),
                        'description': info.get('description', ''),
                        'thumbnail': info.get('thumbnail', ''),
                        'formats': info.get('formats', [])
                    }

        except Exception as error:
            return {
                'status': 'error',
                'message': f'Invalid URL or connection error: {str(error)}'
            }

    def set_download_directory(self, directory: str):
        """Change the download directory"""
        self.download_directory = directory
        os.makedirs(self.download_directory, exist_ok=True)

    def get_download_directory(self) -> str:
        """Get current download directory"""
        return self.download_directory
