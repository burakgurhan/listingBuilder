from typing import Optional
from crewai import Agent
from crewai.project import agent

class EditorAgent:
    """
    A class that creates and configures a write agent for e-commerce title and description builder.
    
    This agent analyzes product data, determines valuable keywords and writes SEO-Friendly product title and description
    """

    def __init__(self):
        """Initialize the ResearcherAgent with necessary API keys and tools."""
        
    
    def create_editor_agent(self, custom_goal: Optional[str] = None) -> Agent:
        """
        Create and configure a title and description builder agent with specific role and capabilities.
        
        Args:
            custom_goal: Optional custom goal for the agent (overrides default)
        
        Returns:
            A configured Agent instance ready to perform market research tasks
        """
        default_goal = ("""Use the reports that comes from Scraper and Researcher agents to write SEO friendly product title and description.""")
        
        try:
            return Agent(
                #llm=self.llm,
                role="SEO Expert",
                backstory="""
                You are an expert Title builder with extensive experience in e-commerce.
                You're known for your exceptional creativity and language skills that put products in the spotlight.
                You understand product specifications, product details, and competitive positioning.
                
                Your process includes:
                1. Analyzing product details received from the Scraper and Researcher Agent
                2. Identifying main keywords the product competes for
                3. Conducting competitor analysis to identify rival products
                4. Write a product title that is SEO friendly and understandable by customers.
                5. Write a product description that contains competitive keywords and easy to understand by customers.
                """,
                goal=custom_goal or default_goal,
                verbose=True
            )
        except Exception as e:
            raise RuntimeError(f"Error creating editor agent: {e}")