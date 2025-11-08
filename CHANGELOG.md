# Changelog

All notable changes to OmniTool will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **UI File System** - Qt Designer support for visual UI design
  - `UILoader` class for loading .ui files (`core/ui_loader.py`)
  - `UIFileWindow` base class for easy UI file integration
  - Support for all Qt Designer features and widgets
  - Signal connection system
  - Widget access by object name
  - Complete Qt Designer workflow support
  - YouTube Downloader .ui file (`ui_files/youtube_downloader.ui`)
  - UI File implementation (`tools/youtube_downloader/window_ui_file.py`)
  - Complete UI File Guide (`docs/UI_FILE_GUIDE.md`)
  - UI files directory with README (`ui_files/README.md`)
  
- **UI Template System** - JSON/YAML-based UI configuration
  - Separate UI configuration from business logic using JSON/YAML templates
  - `UIBuilder` class for template-based UI generation (`core/ui_builder.py`)
  - Support for all common PyQt6 widgets (labels, buttons, inputs, etc.)
  - Flexible layout system (vertical, horizontal, grid)
  - Theme and styling configuration in templates
  - Widget callback system for event handling
  - `ui_templates/` directory for storing UI templates
  - Complete UI Template Guide (`docs/UI_TEMPLATE_GUIDE.md`)
  - Example template for quick start (`ui_templates/example_tool.json`)
  - YouTube Downloader template-based implementation (`tools/youtube_downloader/window_template.py`)
  
### Changed
- YouTube Downloader now uses Qt Designer .ui file by default
- Updated Developer Guide with both UI systems
- Enhanced tool creation workflow with multiple UI options

### Benefits
- 🎨 **Visual Design**: Drag-and-drop UI creation with Qt Designer
- 🏭 **Industry Standard**: Professional Qt development workflow
- 📝 **Easy Maintenance**: Update UI without code changes
- ⚡ **Rapid Development**: Create UIs in minutes
- 🔧 **Flexibility**: Choose between visual (.ui) or template (JSON) approach
- 📖 **Well Documented**: Complete guides for both systems

**UI Template System** - Revolutionary new way to build tool interfaces
  - Separate UI configuration from business logic using JSON/YAML templates
  - `UIBuilder` class for template-based UI generation (`core/ui_builder.py`)
  - Support for all common PyQt6 widgets (labels, buttons, inputs, etc.)
  - Flexible layout system (vertical, horizontal, grid)
  - Theme and styling configuration in templates
  - Widget callback system for event handling
  - `ui_templates/` directory for storing UI templates
  - Complete UI Template Guide (`docs/UI_TEMPLATE_GUIDE.md`)
  - Example template for quick start (`ui_templates/example_tool.json`)
  - YouTube Downloader template-based implementation (`tools/youtube_downloader/window_template.py`)
  
### Changed
- YouTube Downloader now uses template-based UI by default
- Updated Developer Guide with UI template system documentation
- Enhanced tool creation workflow with template option

### Benefits
- 🎨 Easy UI customization without code changes
- 🔧 Separation of concerns (UI vs logic)
- ⚡ Rapid prototyping of tool interfaces
- 📝 Maintainable and reusable UI patterns
- 🎓 Lower barrier to entry for new developers

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
