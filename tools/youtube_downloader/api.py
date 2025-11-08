#!/usr/bin/env python3
"""
Python API wrapper for Electron frontend
Provides JSON-based interface to YouTube downloader functionality
"""

import sys
import json
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.youtube_downloader.downloader import YouTubeDownloader


class DownloaderAPI:
    """API wrapper for YouTube downloader"""
    
    def __init__(self):
        self.downloader = YouTubeDownloader()
    
    def get_video_info(self, url):
        """Get video information"""
        try:
            info = self.downloader.get_video_info(url)
            
            return {
                'success': True,
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'view_count': info.get('view_count', 0),
                'uploader': info.get('uploader', 'Unknown'),
                'description': info.get('description', ''),
                'thumbnail': info.get('thumbnail', ''),
                'formats': self._get_available_formats(info)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def download_video(self, url, quality, format_type, output_path):
        """Download video with progress reporting"""
        try:
            # Set the download directory
            self.downloader.set_download_directory(output_path)
            
            # Set progress callback
            def progress_callback(data):
                """Report progress to stdout as JSON"""
                status = data.get('status', 'downloading')
                print(json.dumps({
                    'status': status,
                    'percent': data.get('percentage', 0),
                    'speed': data.get('speed', 'N/A'),
                    'eta': data.get('eta', 0)
                }), flush=True)
            
            self.downloader.set_progress_callback(progress_callback)
            
            # Download based on format type
            if format_type == 'audio' or format_type == 'mp3':
                result = self.downloader.download_audio(url)
            else:
                result = self.downloader.download_video(url, quality)
            
            if result.get('status') == 'success':
                return {
                    'success': True,
                    'message': result.get('message', 'Download completed')
                }
            else:
                return {
                    'success': False,
                    'error': result.get('message', 'Download failed')
                }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_available_formats(self, info):
        """Extract available formats from video info"""
        formats = []
        
        if 'formats' in info:
            seen_qualities = set()
            for fmt in info['formats']:
                height = fmt.get('height')
                if height and height not in seen_qualities:
                    seen_qualities.add(height)
                    formats.append({
                        'quality': f'{height}p',
                        'format': fmt.get('ext', 'mp4')
                    })
        
        return formats


def main():
    """Main entry point for API"""
    parser = argparse.ArgumentParser(description='YouTube Downloader API')
    parser.add_argument('--get-info', help='Get video information')
    parser.add_argument('--download', action='store_true', help='Download video')
    parser.add_argument('--url', help='Video URL')
    parser.add_argument('--quality', default='best', help='Video quality')
    parser.add_argument('--format', default='mp4', help='Video format')
    parser.add_argument('--output', default='~/Downloads', help='Output directory')
    
    args = parser.parse_args()
    api = DownloaderAPI()
    
    try:
        if args.get_info:
            result = api.get_video_info(args.get_info)
            print(json.dumps(result))
        
        elif args.download:
            if not args.url:
                print(json.dumps({'success': False, 'error': 'URL required'}))
                sys.exit(1)
            
            result = api.download_video(
                url=args.url,
                quality=args.quality,
                format_type=args.format,
                output_path=args.output
            )
            print(json.dumps(result))
        
        else:
            print(json.dumps({'success': False, 'error': 'No action specified'}))
            sys.exit(1)
    
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}))
        sys.exit(1)


if __name__ == '__main__':
    main()
