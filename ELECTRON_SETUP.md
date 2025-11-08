# 🚀 OmniTool Electron Setup Guide

## Prerequisites Installation

### 1. Install Node.js and npm

**Ubuntu/Debian:**
```bash
# Install Node.js 20.x LTS
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

**Using nvm (recommended):**
```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Restart terminal or run:
source ~/.bashrc

# Install Node.js
nvm install 20
nvm use 20

# Verify
node --version
npm --version
```

### 2. Install Python Dependencies (if not already done)

```bash
cd /home/ziadmoh/PycharmProjects/OmniTool
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 📦 Project Setup

### Step 1: Install Node.js Dependencies

```bash
cd /home/ziadmoh/PycharmProjects/OmniTool
npm install
```

This will install:
- electron
- electron-builder
- python-shell

### Step 2: Test the Application

**Development mode (with DevTools for debugging):**
```bash
npm run dev
```

**Production mode:**
```bash
npm start
```

## 🎨 Project Structure

```
OmniTool/
├── electron/                  # Electron main process files
│   ├── main.js               # Main process entry point
│   └── preload.js            # Security bridge (context isolation)
│
├── web/                      # Frontend files (HTML/CSS/JS)
│   ├── index.html           # Main UI
│   ├── css/
│   │   └── styles.css       # Styling
│   └── js/
│       └── app.js           # Frontend logic
│
├── tools/
│   └── youtube_downloader/
│       ├── api.py           # Python API wrapper for Electron
│       ├── downloader.py    # Core download logic
│       └── ...
│
├── package.json             # Node.js configuration
├── requirements.txt         # Python dependencies
└── README.md
```

## 🔧 How It Works

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Electron App                             │
│                                                              │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │  Renderer Process│◄───────►│   Main Process   │         │
│  │  (Web UI)        │   IPC   │   (main.js)      │         │
│  │  HTML/CSS/JS     │         │                  │         │
│  └──────────────────┘         └────────┬─────────┘         │
│                                         │                    │
│                                         │ python-shell       │
│                                         ▼                    │
│                              ┌──────────────────┐           │
│                              │  Python Backend  │           │
│                              │  (api.py)        │           │
│                              │  yt-dlp          │           │
│                              └──────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### Communication Flow

1. **User interaction** → Frontend (web/js/app.js)
2. **Frontend** → IPC call via `window.api.*` (preload.js)
3. **Main Process** → Receives IPC, calls Python via python-shell
4. **Python API** → Executes yt-dlp, returns JSON
5. **Main Process** → Sends result back to Frontend
6. **Frontend** → Updates UI

## 🎯 Key Features

### Why Electron?

✅ **Easy UI Customization**: Use HTML/CSS/JS instead of complex Qt Designer
✅ **Modern Look**: Beautiful, responsive web-based interface  
✅ **Cross-Platform**: Same code works on Linux, Windows, macOS
✅ **Developer Tools**: Built-in Chrome DevTools for debugging
✅ **Rich Ecosystem**: Thousands of npm packages available
✅ **Hot Reload**: Quick iteration during development

### Current Features

- ✅ YouTube video information fetching
- ✅ Multiple quality options (4K, 2K, 1080p, 720p, etc.)
- ✅ Multiple formats (MP4, WebM, MP3, M4A, Opus)
- ✅ Custom download directory selection
- ✅ Real-time download progress
- ✅ Large thumbnail preview
- ✅ Video metadata (title, views, duration, author)
- ✅ Modern, responsive UI

## 🎨 Customizing the UI

### Change Colors

Edit `web/css/styles.css`:

```css
:root {
    --primary-color: #6c5ce7;      /* Purple - change to your color */
    --secondary-color: #00b894;    /* Green - change to your color */
    --bg-dark: #1a1a2e;           /* Dark background */
    --bg-light: #16213e;          /* Lighter background */
}
```

### Modify Layout

Edit `web/index.html` - it's just standard HTML!

### Add Functionality

Edit `web/js/app.js` - it's vanilla JavaScript, no framework needed!

### Example: Add a Button

**1. Add to HTML** (`web/index.html`):
```html
<button id="myButton" class="btn btn-primary">Click Me</button>
```

**2. Add styling** (`web/css/styles.css`):
```css
#myButton {
    /* Your custom styles */
}
```

**3. Add functionality** (`web/js/app.js`):
```javascript
document.getElementById('myButton').addEventListener('click', () => {
    alert('Button clicked!');
});
```

## 🔌 Adding New Features

### Example: Add Playlist Support

**1. Update Python API** (`tools/youtube_downloader/api.py`):
```python
def get_playlist_info(self, url):
    # Add playlist extraction logic
    pass
```

**2. Add IPC Handler** (`electron/main.js`):
```javascript
ipcMain.handle('get-playlist-info', async (event, url) => {
    // Call Python API
});
```

**3. Expose to Frontend** (`electron/preload.js`):
```javascript
contextBridge.exposeInMainWorld('api', {
    // ... existing methods
    getPlaylistInfo: (url) => ipcRenderer.invoke('get-playlist-info', url)
});
```

**4. Use in Frontend** (`web/js/app.js`):
```javascript
const playlist = await window.api.getPlaylistInfo(url);
```

## 🚀 Building for Distribution

### Build for Your Platform

```bash
# Linux (AppImage + .deb)
npm run build:linux

# Windows (.exe installer)
npm run build:win

# macOS (.dmg)
npm run build:mac
```

Output will be in the `dist/` directory.

### Build Configuration

Edit `package.json` → `build` section to customize:
- App name
- Icon
- Installer options
- File associations
- Auto-update settings

## 🐛 Debugging

### Frontend Debugging
1. Run with `npm run dev`
2. DevTools will open automatically
3. Use Console, Network, Elements tabs

### Python Debugging
1. Add print statements in `tools/youtube_downloader/api.py`
2. Output appears in the terminal running Electron
3. Check for JSON parsing errors

### IPC Debugging
1. Add `console.log()` in `electron/main.js`
2. Add `console.log()` in `web/js/app.js`
3. Verify data flow in both directions

## 📋 Comparison: PyQt6 vs Electron

| Feature | PyQt6 | Electron |
|---------|-------|----------|
| UI Technology | Qt Widgets (.ui files) | HTML/CSS/JS |
| Learning Curve | Steep (Qt Designer + Python) | Easy (web technologies) |
| Customization | Limited, needs Qt knowledge | Unlimited, like a website |
| Performance | Native, faster | Slightly slower |
| File Size | ~50-100 MB | ~150-200 MB (includes Chromium) |
| Developer Tools | Limited | Chrome DevTools |
| Cross-Platform | Good | Excellent |
| Hot Reload | No | Yes (with nodemon) |
| Package Size | Smaller | Larger |

## 🎓 Learning Resources

**Electron:**
- [Official Docs](https://www.electronjs.org/docs)
- [Electron Fiddle](https://www.electronjs.org/fiddle) - Interactive playground

**Modern CSS:**
- [CSS Tricks](https://css-tricks.com/)
- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS)

**JavaScript:**
- [JavaScript.info](https://javascript.info/)
- [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)

## 🔐 Security Notes

- ✅ `contextIsolation: true` - Protects from code injection
- ✅ `nodeIntegration: false` - Prevents Node.js in renderer
- ✅ Preload script - Safely exposes only needed APIs
- ✅ IPC validation - Verify inputs in main process

## 💡 Tips & Tricks

### Fast Refresh During Development
```bash
# Install nodemon for auto-restart
npm install --save-dev nodemon

# Update package.json scripts:
"dev": "nodemon --exec electron . --dev"
```

### Reduce Bundle Size
- Use `electron-builder` compression
- Remove unused dependencies
- Optimize images and assets

### Better Error Handling
```javascript
// In web/js/app.js
try {
    const result = await window.api.getVideoInfo(url);
} catch (error) {
    console.error('Detailed error:', error);
    alert(`Error: ${error.message}`);
}
```

## ❓ FAQ

**Q: Can I still use the PyQt6 version?**  
A: Yes! The PyQt6 code is still in the repository. Just run `python main.py`.

**Q: Which version should I use?**  
A: Electron for easier UI customization, PyQt6 for native performance.

**Q: Can I add more tools?**  
A: Absolutely! Follow the same pattern - Python API + IPC handlers + Frontend UI.

**Q: Do I need to know React/Vue/Angular?**  
A: No! The UI uses vanilla JavaScript. But you can add a framework if you want.

**Q: How do I package with the Python environment?**  
A: Use `electron-builder` with custom `extraResources` to include `.venv`.

## 🆘 Troubleshooting

**Node.js not found:**
```bash
# Install using nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 20
```

**npm install fails:**
```bash
# Clear cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Python API errors:**
```bash
# Reinstall yt-dlp
source .venv/bin/activate
pip install --upgrade yt-dlp
```

**Electron won't start:**
```bash
# Check logs
npm start 2>&1 | tee electron.log
```

---

**Ready to start? Run these commands:**

```bash
# Install Node.js first (if not installed)
# Then:
cd /home/ziadmoh/PycharmProjects/OmniTool
npm install
npm run dev
```

**Enjoy your modern Electron app! 🎉**
