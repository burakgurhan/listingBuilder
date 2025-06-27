from typing import Optional
from crewai import Agent
from crewai.project import agent

class ResearcherAgent:
    """
    A class that creates and configures a market research agent for e-commerce competitive analysis.
    
    This agent analyzes product data, identifies competitors, and determines valuable keywords
    for product positioning in the market.
    """

    def __init__(self, web_search_tool):
        """Initialize the ResearcherAgent with necessary API keys and tools."""
        self.web_search_tool = web_search_tool

    
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
                tools=[self.web_search_tool],
                verbose=True
            )
        except Exception as e:
            raise RuntimeError(f"Error creating researcher agent: {e}")