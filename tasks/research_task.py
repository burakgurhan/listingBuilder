import os
from crewai import Task
from agents.researcher_agent import ResearcherAgent
class ResearchTask:
    def __init__(self):
        pass

    def create_research_task(self):
        return Task(
            description="""
    Take the dictionary from the previous agent and analyze the product information.  
    Your goal is to research and extract valuable insights about the product, its market, and competitors.  

    ### Step 1: Product Analysis  
    - Identify the **main keywords and phrases** that describe the product.  
    - Determine the **key features** that differentiate the product.  
    - Define the **target audience** (demographics, interests, potential buyers).  
    - Identify **direct and indirect competitors** in the market.  

    ### Step 2: Market Research  
    - Search the web for **trending and high-value keywords** relevant to the product.  
    - Analyze competitor products and extract the **main keywords they use**.  
    - Research the target audience’s language, pain points, and the **keywords they engage with**.  

    ### Step 3: Report Generation  
    - Compile findings into a structured report.  
    - Include keyword insights, competitor analysis, and audience research.  
    - Pass the final report to the next agent for further processing.  
    """,
    expected_output="""
    A structured report in dictionary format:
    {
        "product_keywords": ["...", "..."],
        "key_features": ["...", "..."],
        "target_audience": "...",
        "competitors": ["...", "..."],
        "trending_keywords": ["...", "..."],
        "competitor_keywords": ["...", "..."],
        "audience_keywords": ["...", "..."]
    }
    """,
    agent=ResearcherAgent().create_researcher_agent()
        )
