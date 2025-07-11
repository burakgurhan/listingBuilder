from crewai.tools import BaseTool

class CustomTools(BaseTool):
    name: str = "Custom Tool"
    description: str = "A custom tool for demonstration purposes."

    def _run(self, argument: str) -> str:
        """
        This is where the logic of your tool goes.
        You can use any Python code here.
        """
        return f"Custom Tool executed with argument: {argument}"
    
from typing import Tuple, Dict, Any
#from crewai import TaskOutput

def validate_product_info(result: dict) -> Tuple[bool, Dict[str, Any]]:
    """
    Validate the product information extracted by the scraper.
    
    Args:
        result (TaskOutput): The output from the scraping task.
        
    Returns:
        Tuple[bool, Dict[str, Any]]: A tuple containing a boolean indicating success and a dictionary with validation details.
    """
    if not result or not isinstance(result):
        return False, {"error": "Invalid result format"}

    product_info = result.data.get('product_info', {})
    
    if not product_info:
        return False, {"error": "No product information found"}
    
    # Example validation logic
    if 'name' not in product_info or 'price' not in product_info:
        return False, {"error": "Missing required fields in product information"}
    
    return True, {"message": "Product information is valid", "data": product_info}

def validate_writing_output(result: dict) -> Tuple[bool, Any]:
    """
    Validate the writing output from the writer task.
    
    Args:
        result (TaskOutput): The output from the writing task.
        
    Returns:
        Tuple[bool, Dict[str, Any]]: A tuple containing a boolean indicating success and a dictionary with validation details.
    """
    if not result or not isinstance(result):
        return False, {"error": "Invalid result format"}

    writing_output = result.data.get('writing_output', {})
    
    if not writing_output:
        return False, {"error": "No writing output found"}
    
    # Example validation logic
    if 'content' not in writing_output or 'summary' not in writing_output:
        return False, {"error": "Missing required fields in writing output"}
    
    return True, {"message": "Writing output is valid", "data": writing_output}