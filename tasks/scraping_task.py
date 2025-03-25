import os
from crewai import Task
from crewai.project import task
from agents.scraper_agent import ScraperAgent
class ScrapingTask:
    def __init__(self, url):
        self.url = url

    def create_scraping_task(self):
        return Task(
            name="Scraping Task",
            description="""
    Scrape the product information from the given web page URL.  
    Extract the following details:  
    - **Title**: The name of the product.  
    - **Description**: A brief summary of the product.  
    - **Color**: The available colors of the product.  
    - **Size**: The dimensions or size variations of the product.  
    - **Count**: The number of items included in a package.  

    Additionally:    
    - Analyze the extracted information to determine the **type of product** and its potential use.  
    - Structure the data into a dictionary format.  
    - Ensure the extracted data is clean and formatted correctly. 
    - If the information is not available, fill in the missing fields with a default value.
    - Provide the collected information to the next agent for further processing.  

    Do not invent or create new data. Only extract the information from the given web page.
    Here is the url: {self.url}
    """,
    expected_output="""
    A dictionary containing the product information:
    {
        "title": "...",
        "description": "...",
        "color": "...",
        "size": "...",
        "count": "...",
        "product_type": "..."
    }
    """,
    agent=ScraperAgent().create_scraper_agent()
        )
