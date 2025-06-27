from crewai import Task
from initial_demo.agents.scraper_agent import ScraperAgent # Updated import path
from crewai.project import task
from urllib.parse import urlparse, urlunparse

class ScrapingTask:
    def __init__(self, url, web_scrape_tool, web_search_tool):
        self.url = url
        self.validate_url(self.url)  # Validate the URL
        self.web_scrape_tool = web_scrape_tool
        self.web_search_tool = web_search_tool

    def validate_url(self, url):
        """Ensure the URL is valid and contains a scheme (http/https)."""
        parsed_url = urlparse(url)

        if not parsed_url.scheme:
            print(f"⚠️ Warning: No scheme detected in URL '{url}'. Adding 'https://'.")
            url = f"https://{url}"  # Automatically fix it

        parsed_url = urlparse(url)  # Re-parse the fixed URL
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError(f"🚨 Invalid URL: {url}")

        self.url = url  # Store the corrected URL
    
    def create_scraping_task(self):
        return Task(
            name="Scraping Task",
            description=f"""
    Scrape the product information from the given web page URL.  
    Extract the following details:  
    - **Title**: The name of the product.  
    - **Description**: Description or bullet-points of the product.  
    - **Category**: The main category of the product.  
    - **Color**: The available colors of the product.  
    - **Size**: The dimensions or size variations of the product.  
    - **Count**: The number of items included in a package.  

    Additionally:    
    - Structure the data into a dictionary format.  
    - Ensure the extracted data is clean and formatted correctly. 
    - If the information is not available, fill in the missing fields with None.
    - Provide the collected information to the next agent for further processing.  

    Do not invent or create new data. Only extract the information from the given web page.
    Here is the url: **{self.url}**
    """,
    expected_output="""
    A dictionary containing the product information:
    {
        "title": "...",
        "description": "...",
        "category": "...",
        "color": "...",
        "size": "...",
        "count": "..."
    }
    """,
    agent=ScraperAgent(self.web_scrape_tool, self.web_search_tool).create_scraper_agent(),
    tools=[self.web_scrape_tool, self.web_search_tool]
        )
