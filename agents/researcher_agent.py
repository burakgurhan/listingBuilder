import os
import warnings
from typing import Optional
from dotenv import load_dotenv
from crewai import Agent, LLM
from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool

# Suppress non-critical warnings
warnings.filterwarnings("ignore")

# Load environment variables from .env file
load_dotenv()


class ResearcherAgent:
    """
    A class that creates and configures a market research agent for e-commerce competitive analysis.
    
    This agent analyzes product data, identifies competitors, and determines valuable keywords
    for product positioning in the market.
    """

    def __init__(self):
        """Initialize the ResearcherAgent with necessary API keys and tools."""
        # Get API key from environment variables
        self.api_key = os.environ.get("GROQ_API_KEY")
        
        # Validate API key
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found or empty in .env file")
            
        # Initialize tools
        self.website_search = WebsiteSearchTool()
        self.scrape_web = ScrapeWebsiteTool()

    def get_llm(self, model_name: str = "groq/llama-3.3-70b-versatile",
                temperature: float = 0.3) -> LLM:
        """
        Create and configure a Language Learning Model instance.
        
        Args:
            model_name: The name of the model to use (default: groq/llama-3.3-70b-versatile)
            temperature: Controls randomness in responses (default: 0.3)
                         Lower values are more deterministic, higher values more creative
        
        Returns:
            An initialized LLM instance ready for use by agents
        """
        try:
            return LLM(
                model=model_name,
                temperature=temperature,
                api_key=self.api_key
            )
        except Exception as e:
            raise RuntimeError(f"Error initializing LLM: {e}")

    def create_researcher_agent(self, custom_goal: Optional[str] = None) -> Agent:
        """
        Create and configure a market researcher agent with specific role and capabilities.
        
        Args:
            custom_goal: Optional custom goal for the agent (overrides default)
        
        Returns:
            A configured Agent instance ready to perform market research tasks
        """
        default_goal = ("Analyze product data, identify competitors, and determine the most "
                        "valuable and trending keywords for optimal market positioning.")
        
        try:
            return Agent(
                llm=self.get_llm(),
                role="Market Researcher",
                backstory="""
                You are an expert market researcher with extensive experience in e-commerce competition analysis.
                You're known for your exceptional attention to detail and ability to identify 
                valuable insights from product listings that others might miss.
                You understand product specifications, pricing patterns, and competitive positioning.
                
                Your process includes:
                1. Analyzing product details received from the Scraper Agent
                2. Identifying main keywords the product competes for
                3. Conducting competitor analysis to identify rival products
                4. Extracting keywords used by competitors
                5. Researching trending and high-value keywords in the market
                """,
                goal=custom_goal or default_goal,
                tools=[self.scrape_web, self.website_search],
                verbose=True
            )
        except Exception as e:
            raise RuntimeError(f"Error creating researcher agent: {e}")