from typing import Callable, Any


class ToolRegistry:
    """
    Central registry for UNISERVE execution tools.

    Agents can request tools by name without knowing
    how each tool is implemented.
    """

    def __init__(self):
        self._tools: dict[str, Callable[..., Any]] = {}
        self._descriptions: dict[str, str] = {}

    def register(
        self,
        name: str,
        description: str,
        function: Callable[..., Any],
    ):
        """Register a callable tool."""
        self._tools[name] = function
        self._descriptions[name] = description

    def execute(self, name: str, **kwargs):
        """Execute a registered tool."""
        if name not in self._tools:
            raise ValueError(f"Tool not found: {name}")

        return self._tools[name](**kwargs)

    def list_tools(self):
        """Return available tools and descriptions."""
        return [
            {
                "name": name,
                "description": self._descriptions[name],
            }
            for name in self._tools
        ]

    def has_tool(self, name: str) -> bool:
        return name in self._tools