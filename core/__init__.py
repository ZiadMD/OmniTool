"""
OmniTool Core Package
Clean architecture with design patterns
"""

from .base_tool import BaseTool
from .tool_registry import ToolRegistry
from .app_manager_clean import AppManager, ToolCategory

__version__ = "0.1.0"
__all__ = ['BaseTool', 'ToolRegistry', 'AppManager', 'ToolCategory', '__version__']
