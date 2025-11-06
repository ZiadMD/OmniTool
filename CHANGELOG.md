# Changelog

All notable changes to OmniTool will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-11-06

### Added
- Initial release of OmniTool multi-tool launcher
- Beautiful PyQt6-based card launcher interface with search and category filtering
- Clean architecture with design patterns (Registry, Template Method, Facade, Decorator)
- Plugin system for automatic tool discovery via `@ToolRegistry.register`
- Core framework (`core/base_tool.py`, `core/tool_registry.py`, `core/app_manager_clean.py`)
- YouTube Downloader tool with the following features:
  - Video and audio download support
  - Multiple quality options (240p to 4K)
  - MP3 audio extraction
  - Thumbnail preview
  - Real-time progress tracking
  - Custom download directory selection
- Comprehensive documentation:
  - User guide for launcher and tools usage
  - Developer guide with 3-step tool creation process
- Educational license for learning purposes
- Modern UI with search functionality across tool names, descriptions, and keywords
- Category-based tool organization
- Error handling and user feedback systems

### Technical Details
- Python 3.8+ compatibility
- PyQt6 6.6+ GUI framework
- yt-dlp integration for media downloading
- FFmpeg support for media processing
- Clean project structure with separation of concerns
- Template-based tool development system

### Dependencies
- PyQt6 >= 6.6
- yt-dlp (for YouTube downloader)
- FFmpeg (system dependency for media tools)

### Documentation
- Complete README.md with installation and usage instructions
- Developer guide for adding new tools
- User guide for application usage
- Architecture follows clean coding principles

---

## Release Notes

This is the initial public release of OmniTool. The project provides a solid foundation for building and organizing small utility tools under a unified launcher interface.

**What's Ready:**
- ✅ Stable launcher interface
- ✅ Working YouTube downloader tool
- ✅ Plugin system for easy tool addition
- ✅ Complete documentation

**Next Steps:**
- Add more bundled tools
- Improve error handling
- Add automated tests
- Create installer packages
