import os
import warnings
from dotenv import load_dotenv
from crewai import Agent, LLM
from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool

warnings.filterwarnings("ignore")
load_dotenv()

class ScraperAgent:
    def __init__(self):
        self.groq_api_key = os.environ["GROQ_API_KEY"]
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        self.website_search = WebsiteSearchTool()
        self.scrape_web = ScrapeWebsiteTool()

    def get_llm(self, model_name: str="groq/llama-3.3-70b-versatile", 
                temperature: float=0.1):
        """
        Args: 
            model_name (str): the name of the model.
            temperature (float): the temperature of the model.
        Returns:
            LLM: An initialized LLM instance
        """
        try:
            return LLM(
                model = model_name,
                temperature = temperature,
                api_key=self.groq_api_key
            )
        except Exception as e:
            raise RuntimeError(f"Error initializing LLM: {e}")
    

    def create_scraper_agent(self):
        # Create the scraper agent
        """
        Create and configure a web scraping agent with specific role and capabilities.
        
        Args:
            custom_goal: Optional custom goal for the agent (overrides default)
        
        Returns:
            A configured Agent instance ready to perform web scraping tasks
        """
        try:
            return Agent(
                llm=self.get_llm(),
                role="Web Scraper",
                backstory="""
                You are an expert web scraper with extensive experience in e-commerce data extraction.
                You're known for your exceptional attention to detail and ability to identify 
                valuable insights from product listings that others might miss.
                You understand product specifications, pricing patterns, and competitive positioning.
            """,
                goal="Your goal is to extract data from product detail pages and then report it to the next agent.",
                tools=[self.scrape_web, self.website_search],
                verbose=True
            )
        except Exception as e:
            raise RuntimeError(f"Error creating scraper agent: {e}")