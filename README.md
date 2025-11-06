# OmniTool - Your All-in-One Toolkit

A modern, comprehensive multi-tool application with a beautiful launcher interface built with **clean architecture** and **design patterns**.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.6+-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-Educational-orange.svg)](LICENSE)

---

## 🌟 What is OmniTool?

OmniTool is a **multi-tool platform** where you can access various productivity tools from a single, elegant launcher. Instead of opening separate applications, launch OmniTool and access everything with one click!

**Features:**
- 🎨 Beautiful card-based launcher interface
- 🔍 Smart search across all tools
- 📂 Category-based organization
- 🚀 One-click tool launching
- 🔧 Easy to extend with new tools

---

## 📸 Screenshot
![Screenshot of the App](assets/Images/App%20Screenshot.png)

---

## 🚀 Quick Start

### Installation

```bash
# 1. Clone or navigate to project
cd /home/ziadmoh/PycharmProjects/OmniTool

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install FFmpeg (for media tools)
sudo apt install ffmpeg  # Ubuntu/Debian
```

### Launch

```bash
# Launch the main launcher
python main.py

# Launch a specific tool directly
python main.py --tool youtube_downloader

# Launch CLI mode
python main.py --cli
```

---

## 🛠️ Available Tools

### ✅ Fully Functional
- **🎬 YouTube Downloader** - Download videos/audio with quality selection and thumbnails

### 🔜 Coming Soon (Template Ready)
Add your own tools easily! See [Developer Guide](docs/DEVELOPER_GUIDE.md)

---

## 📖 Documentation

All documentation is organized in the **[docs/](docs/)** directory:

### For Users
- **[Quick Start Guide](docs/QUICKSTART.md)** - Get started in 5 minutes
- **[Complete User Guide](docs/OMNITOOL_GUIDE.md)** - All features explained

### For Developers
- **[Quick Add Tool Guide](docs/QUICK_ADD_TOOL.md)** ⭐ - Add tools in 3 steps
- **[Developer Guide](docs/DEVELOPER_GUIDE.md)** - Complete development docs
- **[Architecture Guide](docs/ARCHITECTURE.md)** - Design patterns & structure

### Browse All Docs
- **[Documentation Index](docs/README.md)** - Full documentation navigation

---

## 🏗️ Project Structure

```
OmniTool/
├── main.py                  # Entry point
├── launcher_clean.py        # Main launcher UI
├── requirements.txt         # Dependencies
├── README.md               # This file
│
├── core/                   # Framework core
│   ├── base_tool.py       # Tool interface
│   ├── tool_registry.py   # Auto-discovery
│   └── app_manager_clean.py # Manager
│
├── tools/                  # All tools here
│   └── ytDownloader/      # Example tool
│       ├── tool.py        # Tool registration
│       ├── pyqt_gui.py    # UI implementation
│       └─��� downloader.py  # Business logic
│
└── docs/                   # Documentation
    ��── README.md          # Docs index
    ├── QUICKSTART.md      # User guide
    ├── DEVELOPER_GUIDE.md # Dev guide
    └── ...               # More docs
```

---

## ⚡ Adding New Tools (Super Easy!)

Create a new tool in **3 simple steps**:

```bash
# 1. Create directory
mkdir tools/myTool && touch tools/myTool/__init__.py
```

```python
# 2. Create tools/myTool/tool.py
from core.base_tool import BaseTool
from core.tool_registry import ToolRegistry
from PyQt6.QtWidgets import QMainWindow

@ToolRegistry.register
class MyTool(BaseTool):
    def get_metadata(self) -> dict:
        return {
            'id': 'my_tool',
            'name': 'My Tool',
            'description': 'What it does',
            'category': 'Utilities',
            'icon': '🔧',
            'keywords': ['my', 'tool'],
            'version': '1.0.0',
            'author': 'Your Name'
        }
    
    def create_window(self) -> QMainWindow:
        # Create and return your UI window
        pass
```

```bash
# 3. Launch and see it appear!
python main.py
```

**That's it!** Your tool appears automatically in the launcher.

📖 **Full Guide:** [docs/QUICK_ADD_TOOL.md](docs/QUICK_ADD_TOOL.md)

---

## 🎨 Design Patterns Used

OmniTool uses professional software design patterns:

- **Template Method** - Consistent tool behavior
- **Registry** - Auto-discovery of tools
- **Facade** - Simple API
- **Singleton** - Centralized management
- **Decorator** - Clean tool registration

Learn more: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 🧪 Requirements

- Python 3.7+
- PyQt6 6.6+
- yt-dlp (for YouTube tool)
- FFmpeg (for media tools)

See [requirements.txt](requirements.txt) for full list.

---

## 📝 License

This project is for educational purposes. Individual tools may have their own licenses.

---

## 🤝 Contributing

Contributions are welcome! To add a tool:

1. Follow the [Quick Add Tool Guide](docs/QUICK_ADD_TOOL.md)
2. Test your tool thoroughly
3. Submit a pull request

---

## 🐛 Troubleshooting

### Tool doesn't appear in launcher
- Check that `tool.py` exists
- Verify `@ToolRegistry.register` decorator is used
- Check console for import errors

### Import errors
```bash
pip install -r requirements.txt
```

### More issues?
See [docs/QUICKSTART.md](docs/QUICKSTART.md) troubleshooting section.

---

## 🎯 Next Steps

1. **Launch the app**: `python main.py`
2. **Read the docs**: Check [docs/README.md](docs/README.md)
3. **Add your first tool**: Follow [docs/QUICK_ADD_TOOL.md](docs/QUICK_ADD_TOOL.md)

---

## 📊 Project Stats

- **Architecture**: Clean Architecture with Design Patterns
- **UI Framework**: PyQt6
- **Python Version**: 3.7+
- **Tools**: Extensible plugin system
- **Documentation**: 8 comprehensive guides

---

**Made with ❤️ using Python & PyQt6**

🚀 **Start now:** `python main.py`

