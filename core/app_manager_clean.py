"""
OmniTool - Clean Application Manager
Simplified manager using the Registry Pattern
"""

from typing import List, Dict
from core.tool_registry import ToolRegistry


class ToolCategory:
    """Tool category constants"""
    MEDIA = "Media & Video"
    PRODUCTIVITY = "Productivity"
    UTILITIES = "Utilities"
    NETWORKING = "Networking"
    DEVELOPMENT = "Development"
    SYSTEM = "System Tools"
    OTHER = "Other"


class AppManager:
    """
    Simplified Application Manager.

    Design Pattern: Facade Pattern
    - Provides a simple interface to the complex tool registry
    - Handles tool filtering, searching, and categorization
    """

    def __init__(self):
        """Initialize and discover all tools"""
        self._discover_tools()

    def _discover_tools(self):
        """
        Automatically discover and import all tools.

        Convention: Each tool package must have a tool.py file
        that registers itself with @ToolRegistry.register
        """
        import importlib
        import pkgutil
        import tools

        # Walk through all packages in the tools directory
        for importer, modname, ispkg in pkgutil.walk_packages(
            path=tools.__path__,
            prefix=tools.__name__ + '.',
        ):
            if ispkg:
                # Try to import tool.py from each package
                try:
                    tool_module = f"{modname}.tool"
                    importlib.import_module(tool_module)
                except (ImportError, AttributeError) as e:
                    # Tool doesn't have a tool.py or it has errors
                    pass

    def get_all_tools(self) -> List[dict]:
        """Get metadata for all registered tools"""
        return ToolRegistry.get_tool_metadata_list()

    def get_tools_by_category(self, category: str) -> List[dict]:
        """Get tools filtered by category"""
        all_tools = self.get_all_tools()
        return [t for t in all_tools if t['category'] == category]

    def search_tools(self, query: str) -> List[dict]:
        """Search tools by query"""
        if not query:
            return self.get_all_tools()

        query_lower = query.lower()
        all_tools = self.get_all_tools()
        results = []

        for tool in all_tools:
            # Search in name, description, keywords, and category
            if (query_lower in tool['name'].lower() or
                query_lower in tool['description'].lower() or
                query_lower in tool['category'].lower() or
                any(query_lower in kw.lower() for kw in tool['keywords'])):
                results.append(tool)

        return results

    def get_categories_with_count(self) -> Dict[str, int]:
        """Get all categories with tool counts"""
        all_tools = self.get_all_tools()
        categories = {}

        for tool in all_tools:
            category = tool['category']
            categories[category] = categories.get(category, 0) + 1

        return categories

    def launch_tool(self, tool_id: str):
        """
        Launch a tool by ID.

        Args:
            tool_id: The unique identifier of the tool

        Returns:
            QMainWindow: The tool's window instance, or None if not found
        """
        tool_instance = ToolRegistry.create_tool_instance(tool_id)
        if tool_instance:
            return tool_instance.launch()
        return None

