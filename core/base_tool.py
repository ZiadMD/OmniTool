"""
OmniTool Base Tool Interface
Define the contract that all tools must implement
"""

from abc import ABC, abstractmethod
from typing import Optional
from PyQt6.QtWidgets import QMainWindow


class BaseTool(ABC):
    """
    Abstract base class for all OmniTool tools.
    
    Design Pattern: Template Method Pattern
    - Defines the skeleton of tool operations
    - Subclasses override specific methods
    """
    
    def __init__(self):
        """Initialize the tool"""
        self.window: Optional[QMainWindow] = None
        
    @abstractmethod
    def get_metadata(self) -> dict:
        """
        Return tool metadata for the launcher.
        
        Returns:
            dict: {
                'id': str,           # Unique identifier
                'name': str,         # Display name
                'description': str,  # Brief description
                'category': str,     # Category name
                'icon': str,         # Emoji or icon
                'keywords': list,    # Search keywords
                'version': str,      # Tool version
                'author': str        # Author name
            }
        """
        pass
        
    @abstractmethod
    def create_window(self) -> QMainWindow:
        """
        Create and return the tool's main window.
        
        Returns:
            QMainWindow: The tool's main window instance
        """
        pass
        
    def launch(self) -> QMainWindow:
        """
        Launch the tool (Template Method).
        
        This method orchestrates the tool launch process:
        1. Create window if not exists
        2. Show window
        3. Return window instance
        
        Returns:
            QMainWindow: The tool's window instance
        """
        if self.window is None:
            self.window = self.create_window()
        
        self.window.show()
        return self.window
        
    def cleanup(self):
        """
        Clean up resources when tool is closed.
        Override this method if cleanup is needed.
        """
        if self.window:
            self.window.close()
            self.window = None

