from typing import Tuple, Dict, Any
from crewai import TaskOutput


def validate_product_info(result: TaskOutput) -> Tuple[bool, Dict[str, Any]]:
    """
    Validate the product information extracted by the scraper.
    
    Args:
        result (TaskOutput): The output from the scraping task.
        
    Returns:
        Tuple[bool, Dict[str, Any]]: A tuple containing a boolean indicating success and a dictionary with validation details.
    """
    if not result or not isinstance(result, TaskOutput):
        return False, {"error": "Invalid result format"}

    product_info = result.data.get('product_info', {})
    
    if not product_info:
        return False, {"error": "No product information found"}
    
    # Example validation logic
    if 'name' not in product_info or 'price' not in product_info:
        return False, {"error": "Missing required fields in product information"}
    
    return True, {"message": "Product information is valid", "data": product_info}