"""
OmniTool - Tool Registry
Centralized tool registration using the Registry Pattern
"""

from typing import Dict, List, Type
from core.base_tool import BaseTool


class ToolRegistry:
    """
    Registry Pattern: Centralized tool registration and management.
    
    This class maintains a registry of all available tools and provides
    methods to query and access them.
    """
    
    _instance = None
    _tools: Dict[str, Type[BaseTool]] = {}
    
    def __new__(cls):
        """Singleton Pattern: Ensure only one registry instance exists"""
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
        return cls._instance
        
    @classmethod
    def register(cls, tool_class: Type[BaseTool]):
        """
        Register a tool class.
        
        Args:
            tool_class: A class that inherits from BaseTool
            
        Example:
            @ToolRegistry.register
            class MyTool(BaseTool):
                ...
        """
        # Create temporary instance to get metadata
        temp_instance = tool_class()
        metadata = temp_instance.get_metadata()
        tool_id = metadata['id']
        
        cls._tools[tool_id] = tool_class
        print(f"✓ Registered tool: {metadata['name']} (ID: {tool_id})")
        
        return tool_class
        
    @classmethod
    def get_tool_class(cls, tool_id: str) -> Type[BaseTool]:
        """Get a tool class by ID"""
        return cls._tools.get(tool_id)
        
    @classmethod
    def get_all_tools(cls) -> Dict[str, Type[BaseTool]]:
        """Get all registered tools"""
        return cls._tools.copy()
        
    @classmethod
    def get_tool_metadata_list(cls) -> List[dict]:
        """Get metadata for all registered tools"""
        metadata_list = []
        for tool_class in cls._tools.values():
            instance = tool_class()
            metadata_list.append(instance.get_metadata())
        return metadata_list
        
    @classmethod
    def create_tool_instance(cls, tool_id: str) -> BaseTool:
        """Create an instance of a tool by ID"""
        tool_class = cls.get_tool_class(tool_id)
        if tool_class:
            return tool_class()
        return None

