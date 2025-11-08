# 📚 OmniTool - Quick Reference

## 🚀 Quick Start

```bash
./start.sh
```

Or manually:

```bash
npm start          # Start the app
npm run dev        # Start with DevTools
```

## 📁 Clean Project Structure

```
OmniTool/
├── electron/                  # Electron backend
│   ├── main.js               # Main process, IPC handlers
│   └── preload.js            # Security bridge
│
├── web/                      # Frontend (easy to edit!)
│   ├── index.html           # App shell with sidebar menu
│   ├── css/
│   │   └── styles.css       # All styling in one place
│   ├── js/
│   │   ├── navigation.js    # Page routing
│   │   └── app.js          # Tool functionality
│   └── tools/               # Tool pages (HTML)
│       ├── youtube-downloader.html
│       ├── settings.html
│       └── about.html
│
├── tools/                    # Python backend
│   └── youtube_downloader/
│       ├── api.py           # JSON API for Electron
│       └── downloader.py    # Core logic
│
├── package.json             # Node.js config
├── requirements.txt         # Python dependencies
└── start.sh                 # Quick start script
```

## 🎨 How to Edit

### Change Colors
`web/css/styles.css` - Line 6-15:
```css
:root {
    --primary-color: #6c5ce7;     /* Main purple */
    --secondary-color: #00b894;   /* Green accent */
    --bg-dark: #1a1a2e;          /* Dark bg */
}
```

### Add Menu Item
`web/index.html` - In `<nav class="nav-menu">`:
```html
<a href="#" class="nav-item" data-tool="mytool">
    <span class="nav-icon">🔧</span>
    <span class="nav-text">My Tool</span>
</a>
```

### Create New Tool Page
1. Create `web/tools/mytool.html`
2. Add Python API in `tools/mytool/api.py`
3. Add IPC handler in `electron/main.js`
4. Add navigation logic in `web/js/navigation.js`

### Modify YouTube Downloader
- UI: `web/tools/youtube-downloader.html`
- Logic: `web/js/app.js` → `initYouTubeDownloader()`
- Backend: `tools/youtube_downloader/api.py`

## 🔧 Common Tasks

### Update yt-dlp
```bash
source .venv/bin/activate
pip install --upgrade yt-dlp
```

### Clear Cache
```bash
rm -rf node_modules package-lock.json
npm install
```

### Build for Distribution
```bash
npm run build:linux    # Creates AppImage + .deb
npm run build:win      # Creates .exe installer
npm run build:mac      # Creates .dmg
```

## 🐛 Debugging

### Frontend (Renderer)
1. Run `npm run dev`
2. DevTools open automatically
3. Check Console tab

### Python Backend
1. Add `print()` in `tools/youtube_downloader/api.py`
2. Check terminal output

### IPC Communication
1. Add `console.log()` in `electron/main.js` (main process)
2. Add `console.log()` in `web/js/app.js` (renderer)

## 📝 File Purposes

| File | Purpose |
|------|---------|
| `electron/main.js` | Main Electron process, creates window, handles IPC |
| `electron/preload.js` | Exposes safe APIs to renderer |
| `web/index.html` | App shell with sidebar navigation |
| `web/css/styles.css` | All styles in one file |
| `web/js/navigation.js` | Handles page routing and loading |
| `web/js/app.js` | Tool-specific functionality |
| `tools/*/api.py` | Python API wrapper for each tool |
| `package.json` | Node.js dependencies and scripts |

## 🎯 Key Features

### Sidebar Navigation
- ✅ Automatic active state
- ✅ Smooth page transitions
- ✅ Settings and About pages
- ✅ "Coming Soon" indicators

### YouTube Downloader
- ✅ Video info fetching
- ✅ Multiple qualities (4K to 360p)
- ✅ Multiple formats (MP4, MP3, etc.)
- ✅ Custom download directory
- ✅ Real-time progress
- ✅ Large thumbnail preview

### Settings Page
- ✅ Default download directory
- ✅ Default quality/format
- ✅ Theme selection (ready)
- ✅ Settings persistence (localStorage)

## 💡 Tips

1. **Hot Reload**: After editing `web/` files, just press `Ctrl+R` in the app
2. **DevTools**: Press `F12` or `Ctrl+Shift+I` when running with `npm run dev`
3. **Clean Build**: Run `rm -rf node_modules && npm install` if issues occur
4. **Python Path**: Virtual environment path is hardcoded in `electron/main.js` - adjust if needed

## 🆘 Troubleshooting

**App won't start?**
- Check if Node.js is installed: `node --version`
- Install dependencies: `npm install`

**Download fails?**
- Update yt-dlp: `pip install --upgrade yt-dlp`
- Check Python path in `electron/main.js`

**UI not updating?**
- Hard reload: `Ctrl+Shift+R`
- Check browser console for errors

## 📞 Quick Commands

```bash
npm start              # Start app
npm run dev           # Start with DevTools
npm run build:linux   # Build for Linux
./start.sh            # Auto setup + start
```

---

**Everything is clean, organized, and easy to edit! 🎉**
