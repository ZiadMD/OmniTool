# 👤 OmniTool User Guide

## Getting Started

### Launch OmniTool

```bash
python main.py
```

This opens the main launcher window with all available tools.

---

## 🎛️ Using the Launcher

### Search for Tools
- Type in the search bar to filter tools
- Search works across names, descriptions, and keywords
- Results update in real-time

### Browse by Category
- Click categories in the left sidebar
- **All Tools** - Shows everything
- **Media & Video** - YouTube downloader, converters
- **Productivity** - PDF tools, editors
- **Utilities** - File tools, generators
- **Development** - Code tools

### Launch a Tool
- Click any tool card to open it
- Each tool opens in its own window
- You can run multiple tools simultaneously

---

## 🎬 YouTube Downloader

### Features
- Download videos in multiple qualities (240p to 4K)
- Download audio as MP3
- Thumbnail preview before downloading
- Playlist support
- Real-time progress tracking

### How to Use

1. **Paste URL**
   - Copy a YouTube video or playlist URL
   - Paste it in the URL field
   - Press Enter or click "Get Info"

2. **Preview Video**
   - Thumbnail loads automatically
   - View title, duration, uploader, and views
   - Playlist shows video count

3. **Choose Options**
   - Select **Video** or **Audio (MP3)**
   - For video: Choose quality (Best, 1080p, 720p, etc.)
   - For audio: Quality is automatic (192kbps MP3)

4. **Download**
   - Click "Start Download"
   - Watch progress bar and speed
   - Files save to the displayed directory

5. **Change Save Location**
   - Click "Change" button at the bottom
   - Select your preferred folder
   - All future downloads go there

### Tips
- **Best Available** quality automatically selects the highest quality
- Playlists download all videos sequentially
- Activity log shows detailed progress
- Don't close the window until download completes

### Troubleshooting

**Error: "Invalid URL"**
- Make sure you copied the full YouTube URL
- Supported formats:
  - `https://www.youtube.com/watch?v=VIDEO_ID`
  - `https://youtu.be/VIDEO_ID`
  - Playlist URLs

**Error: "Download failed"**
- Check your internet connection
- Ensure FFmpeg is installed: `ffmpeg -version`
- Try a different quality setting

**Slow Downloads**
- Speed depends on your internet connection
- Try a lower quality for faster downloads
- Some videos have speed limits from YouTube

---

## 💡 Pro Tips

- Use keyboard shortcuts:
  - Enter in URL field = Fetch video info
  - Search bar works instantly as you type
- You can minimize OmniTool while tools are running
- Each tool is independent - close tools you're not using
- Check the Activity Log for detailed information

---

## 🆘 Getting Help

If you encounter issues:
1. Check the Activity Log in each tool
2. Verify all dependencies are installed
3. Restart the application
4. Check [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for technical details

