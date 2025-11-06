# 👨‍💻 OmniTool Developer Guide

## Quick Start: Add a New Tool in 3 Steps

### Step 1: Create Directory Structure

```bash
cd tools/
mkdir my_tool
cd my_tool
touch __init__.py tool.py window.py
```

### Step 2: Create `tool.py` (Registration)

```python
"""
My Tool
Description of what your tool does
"""

from core.base_tool import BaseTool
from core.tool_registry import ToolRegistry
from PyQt6.QtWidgets import QMainWindow


@ToolRegistry.register  # ← This auto-registers your tool!
class MyTool(BaseTool):
    """My tool description"""

    def get_metadata(self) -> dict:
        """Define tool metadata for the launcher"""
        return {
            'id': 'my_tool',                    # Unique identifier (snake_case)
            'name': 'My Tool',                  # Display name
            'description': 'Does amazing things', # Short description
            'category': 'Utilities',            # Category (see below)
            'icon': '🔧',                       # Emoji icon
            'keywords': ['tool', 'utility'],    # Search keywords
            'version': '1.0.0',
            'author': 'Your Name'
        }

    def create_window(self) -> QMainWindow:
        """Create and return the tool's main window"""
        from tools.my_tool.window import MyToolWindow
        return MyToolWindow()
```

### Step 3: Create `window.py` (UI)

```python
"""
My Tool Window
Main UI for My Tool
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QPushButton
)
from PyQt6.QtCore import Qt


class MyToolWindow(QMainWindow):
    """Main window for My Tool"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Tool")
        self.setMinimumSize(800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Add widgets
        title = QLabel("My Tool")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        button = QPushButton("Click Me")
        button.clicked.connect(self.on_button_click)
        layout.addWidget(button)
    
    def on_button_click(self):
        """Handle button click"""
        print("Button clicked!")
```

### Step 4: Export from `__init__.py`

```python
"""
My Tool
"""

from .tool import MyTool
from .window import MyToolWindow

__all__ = ['MyTool', 'MyToolWindow']
```

**That's it!** Your tool is now:
- ✅ Auto-discovered by OmniTool
- ✅ Searchable in the launcher
- ✅ Ready to use

---

## 📐 Architecture

### Design Patterns

**Registry Pattern** - Tools register themselves
```python
@ToolRegistry.register
class MyTool(BaseTool):
    pass
```

**Template Method Pattern** - BaseTool defines the interface
```python
class BaseTool(ABC):
    @abstractmethod
    def get_metadata(self) -> dict:
        pass
    
    @abstractmethod
    def create_window(self) -> QMainWindow:
        pass
```

**Facade Pattern** - AppManager simplifies usage
```python
from core.app_manager_clean import AppManager
app_manager = AppManager()
app_manager.launch_tool('my_tool')
```

### Project Structure

```
OmniTool/
├── main.py                    # Entry point
├── launcher_clean.py          # Main launcher UI
├── core/
│   ├── base_tool.py          # Abstract base class
│   ├── tool_registry.py      # Registry pattern
│   └── app_manager_clean.py  # Facade pattern
└── tools/
    ├── youtube_downloader/
    │   ├── __init__.py
    │   ├── tool.py           # Registration
    │   ├── window.py         # UI
    │   └── downloader.py     # Business logic
    └── your_tool/
        ├── __init__.py
        ├── tool.py
        └── window.py
```

---

## 📝 Metadata Reference

### Categories
Choose from:
- `Media & Video` - Video/audio tools
- `Productivity` - Office, PDF, text tools
- `Utilities` - File managers, generators
- `Development` - Code tools, formatters
- `Graphics & Design` - Image tools, editors
- `System` - System utilities

### Metadata Fields

```python
{
    'id': 'unique_tool_id',           # Required: snake_case, unique
    'name': 'Tool Display Name',      # Required: shown in launcher
    'description': 'Brief description', # Required: 1-2 sentences
    'category': 'Utilities',          # Required: from list above
    'icon': '🔧',                     # Required: emoji
    'keywords': ['key', 'words'],     # Required: for search
    'version': '1.0.0',               # Required: semantic versioning
    'author': 'Your Name'             # Required: your name
}
```

---

## 🎨 UI Best Practices

### Modern Window Design

```python
class MyToolWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Tool")
        self.setMinimumSize(800, 600)  # Minimum size
        self.resize(1000, 700)         # Default size
        
        self._initialize_ui()
        self._apply_styling()
    
    def _initialize_ui(self):
        """Initialize UI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Add your widgets here
    
    def _apply_styling(self):
        """Apply custom styles"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
```

### Using Threading for Long Operations

```python
from PyQt6.QtCore import QThread, pyqtSignal

class WorkerThread(QThread):
    finished = pyqtSignal(dict)
    progress = pyqtSignal(int)
    
    def run(self):
        # Do long-running work
        for i in range(100):
            # ... work ...
            self.progress.emit(i)
        
        self.finished.emit({'status': 'success'})

# In your window:
def start_work(self):
    self.worker = WorkerThread()
    self.worker.progress.connect(self.on_progress)
    self.worker.finished.connect(self.on_finished)
    self.worker.start()
```

---

## 🔧 Advanced Examples

### Tool with Settings

```python
class MyTool(BaseTool):
    def __init__(self):
        self.settings = {
            'default_path': '/home/user/downloads',
            'auto_start': True
        }
    
    def get_metadata(self) -> dict:
        return {...}
    
    def create_window(self) -> QMainWindow:
        window = MyToolWindow()
        window.load_settings(self.settings)
        return window
```

### Tool with Business Logic Separation

```
my_tool/
├── __init__.py
├── tool.py       # Registration only
├── window.py     # UI only
├── core.py       # Business logic
└── utils.py      # Helper functions
```

```python
# tool.py
from core.base_tool import BaseTool
from core.tool_registry import ToolRegistry
from PyQt6.QtWidgets import QMainWindow

@ToolRegistry.register
class MyTool(BaseTool):
    def get_metadata(self) -> dict:
        return {...}
    
    def create_window(self) -> QMainWindow:
        from tools.my_tool.window import MyToolWindow
        return MyToolWindow()

# window.py
from .core import MyToolCore

class MyToolWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.core = MyToolCore()  # Business logic
        self._initialize_ui()

# core.py
class MyToolCore:
    """Business logic for My Tool"""
    def process_data(self, data):
        # ... logic ...
        return result
```

---

## 🧪 Testing Your Tool

```bash
# Test import
python -c "from tools.my_tool import MyTool; print('✓ Import successful')"

# Test registration
python -c "from core.tool_registry import ToolRegistry; print([t['id'] for t in ToolRegistry.get_all_tools()])"

# Launch your tool
python main.py --tool my_tool
```

---

## 📚 Learn from Examples

Study the YouTube Downloader implementation:
- `tools/youtube_downloader/tool.py` - Clean registration
- `tools/youtube_downloader/window.py` - Modern UI with threading
- `tools/youtube_downloader/downloader.py` - Separated business logic

---

## 🐛 Troubleshooting

**Tool doesn't appear in launcher**
- Check `@ToolRegistry.register` decorator is present
- Verify `tool.py` is in the correct location
- Ensure no syntax errors in `tool.py`

**Import errors**
- Check `__init__.py` exports the tool class
- Verify all dependencies are installed
- Use absolute imports: `from tools.my_tool.window import ...`

**UI doesn't display correctly**
- Set minimum window size: `setMinimumSize(800, 600)`
- Check central widget is set: `setCentralWidget(widget)`
- Verify layout is applied to central widget

---

## 💡 Tips

- Keep tool names short and descriptive
- Use descriptive variable names (e.g., `download_button` not `btn1`)
- Prefix private methods with `_` (e.g., `_initialize_ui`)
- Add docstrings to all classes and methods
- Separate UI from business logic
- Use threading for long-running operations
- Handle errors gracefully with try/except
- Show user feedback with progress bars and status messages

---

## 🎓 Next Steps

1. Create your first tool using the template above
2. Study the YouTube Downloader for advanced patterns
3. Experiment with PyQt6 widgets and layouts
4. Share your tools with others!

