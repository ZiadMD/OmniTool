# 📚 OmniTool Documentation

**A modern, extensible multi-tool application platform built with PyQt6**

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
cd /home/ziadmoh/PycharmProjects/OmniTool

# Install dependencies
pip install -r requirements.txt

# Make sure FFmpeg is installed (for YouTube Downloader)
ffmpeg -version  # Check if installed
```

### Running OmniTool

```bash
# Launch the main launcher
python main.py

# Launch a specific tool directly
python main.py --tool youtube_downloader
```

---

## 📖 Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)** - How to use OmniTool and its tools
- **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** - How to create new tools

---

## 🎯 What is OmniTool?

OmniTool is a unified application launcher that combines multiple tools in one beautiful interface:

- **Modern UI** - Card-based interface with search and categories
- **Extensible** - Add new tools in 3 simple steps
- **Smart Search** - Find tools instantly by name or keywords
- **Clean Architecture** - Built with design patterns (Registry, Template Method, Facade)

### Current Tools

- **🎬 YouTube Downloader** - Download videos/audio with quality selection and thumbnail preview

### Add Your Own Tools

Creating a new tool takes less than 5 minutes! See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md).

---

## 🏗️ Architecture Highlights

```
OmniTool/
├── main.py              # Entry point
├── core/                # Framework
│   ├── base_tool.py     # Tool interface
│   ├── tool_registry.py # Auto-discovery
│   └── app_manager_clean.py
└── tools/               # Your tools here
    └── youtube_downloader/
        ├── tool.py      # Registration
        ├── window.py    # UI
        └── downloader.py # Logic
```

**Design Patterns:**
- **Registry Pattern** - Auto-discovers tools with `@ToolRegistry.register`
- **Template Method** - `BaseTool` defines tool lifecycle
- **Facade Pattern** - `AppManager` provides simple API

---

## 📝 License & Contributing

Feel free to extend OmniTool with your own tools!

