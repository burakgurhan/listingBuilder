from crewai import Agent
from crewai.project import agent

class ScraperAgent:
    def __init__(self, web_scrape_tool, web_search_tool):
        self.web_scrape_tool = web_scrape_tool
        self.web_search_tool = web_search_tool

    
    def create_scraper_agent(self):
        """
        Create and configure a web scraping agent with specific role and capabilities.
        
        Args:
            custom_goal: Optional custom goal for the agent (overrides default)
        
        Returns:
            A configured Agent instance ready to perform web scraping tasks
        """

        try:
            return Agent(
                role="Web Scraper",
                backstory="""
                You are an expert web scraper with extensive experience in e-commerce data extraction.
                You're known for your exceptional attention to detail and ability to identify 
                valuable insights from product listings that others might miss.
                You understand product specifications, pricing patterns, and competitive positioning.
                """,
                goal="Your goal is to extract data from product detail pages and then report it to the next agent.",
                tools=[self.web_scrape_tool, self.web_search_tool],
                verbose=True
            )
        except Exception as e:
            raise RuntimeError(f"Error creating scraper agent: {e}")