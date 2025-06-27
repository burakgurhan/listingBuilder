from crewai_tools import BaseTool

class CustomTools(BaseTool):
    name: str = "Custom Tool"
    description: str = "A custom tool for demonstration purposes."

    def _run(self, argument: str) -> str:
        """
        This is where the logic of your tool goes.
        You can use any Python code here.
        """
        return f"Custom Tool executed with argument: {argument}"