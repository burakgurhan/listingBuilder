import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from src.ListingCrew.tools.custom_tools import CustomTools # Updated import path
from dotenv import load_dotenv
load_dotenv()

class ListingCrew:
    def __init__(self):
        self.serper_api_key = os.environ.get("SERPER_API_KEY")
        self.groq_api_key = os.environ.get("GROQ_API_KEY")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")

    def crew(self):
        # Define tools
        web_search_tool = SerperDevTool(api_key=self.serper_api_key)
        web_scrape_tool = ScrapeWebsiteTool()

        # Define agents
        scraper = Agent(
            role='Web Scraper',
            goal='Extract title, description, and bullet points from product detail pages.',
            backstory='You are an expert web scraper with extensive experience in e-commerce data extraction.',
            tools=[web_scrape_tool],
            verbose=True,
            allow_delegation=False
        )

        # Define tasks
        scrape_task = Task(
            description='Scrape the product information from the given web page URL: {url}',
            expected_output='A dictionary containing the product information: {"title": "...", "description": "...", "bullet_points": ["...", "..."]}',
            agent=scraper
        )

        # Create and return the crew
        return Crew(
            agents=[scraper],
            tasks=[scrape_task],
            verbose=2,
            process=Process.sequential
        )