"""
YouTube Downloader Tool
Implements the BaseTool interface for OmniTool
"""

from core.base_tool import BaseTool
from core.tool_registry import ToolRegistry
from PyQt6.QtWidgets import QMainWindow


@ToolRegistry.register
class YouTubeDownloaderTool(BaseTool):
    """YouTube Downloader - Download videos and audio with quality selection"""

    def get_metadata(self) -> dict:
        """Return tool metadata"""
        return {
            'id': 'youtube_downloader',
            'name': 'YouTube Downloader',
            'description': 'Download YouTube videos and audio with quality selection, thumbnail preview, and playlist support',
            'category': 'Media & Video',
            'icon': '🎬',
            'keywords': ['youtube', 'download', 'video', 'audio', 'mp3', 'music', 'playlist', 'thumbnail'],
            'version': '2.0.0',
            'author': 'OmniTool'
        }

    def create_window(self) -> QMainWindow:
        """Create the YouTube Downloader window"""
        from tools.youtube_downloader.window import YouTubeDownloaderWindow
        return YouTubeDownloaderWindow()
