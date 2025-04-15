import os
import time
import litellm
from dotenv import load_dotenv
from crewai import Crew, Process
from crewai.project import agent, task, crew
from langchain_groq import ChatGroq
from agents.scraper_agent import ScraperAgent
from agents.researcher_agent import ResearcherAgent
from agents.editor_agent import EditorAgent
from tasks.scraping_task import ScrapingTask
from tasks.research_task import ResearchTask
from tasks.writing_task import WritingTask
from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool
load_dotenv()

class SEOCrew:
    """A crew responsible for SEO-related tasks including scraping, research, and content writing."""
    def __init__(self, url, max_retries=3):
        """
        Args:
            url (str): The target URL for SEO operations. Must be a valid HTTP/HTTPS URL.
            max_retries (int): The maximum number of retries for failed tasks. Defaults to 3
        """
        self.url = url
        self.max_retries = max_retries
        self.web_search_tool = WebsiteSearchTool()
        self.web_scrape_tool = ScrapeWebsiteTool()
        
        self.groq_api_key = os.environ["GROQ_API_KEY"]
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        
        self.openai_api_key = os.environ["OPENAI_API_KEY"]
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file")
    
    def _create_llm(self, model_name: str="qwen-2.5-32b", temperature: float=0.1):
        """
        Returns a Langchain ChatGroq LLM instance
        Args: 
            model_name (str): the name of the model
            temperature (float): the temperature of the model
        Returns:
            ChatGroq: An initialized Langchain LLM instance
        """
        try:
            return ChatGroq(
                api_key=self.groq_api_key,
                model_name=model_name,   #"mixtral-8x7b-32768",
                temperature=temperature,
            )
        except Exception as e:
            raise RuntimeError(f"Error initializing LLM: {e}")
    
    def _create_tasks(self):
        return [
            ScrapingTask(self.url, self.web_scrape_tool, self.web_search_tool).create_scraping_task(),
            ResearchTask(self.web_search_tool).create_research_task(),
            WritingTask().create_writing_task()
        ]

    def _create_agents(self):
        return [
            ScraperAgent(web_scrape_tool=self.web_scrape_tool, web_search_tool=self.web_search_tool).create_scraper_agent(),  # Use the initialized llm
            ResearcherAgent(web_search_tool=self.web_search_tool).create_researcher_agent(),
            EditorAgent().create_editor_agent()
        ]

    def _retry_with_backoff(self, func, *args, **kwargs):
        """
        Retry a function with exponential backoff for rate limit errors.
        
        Args:
            func (callable): The function to retry
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
        
        Returns:
            The result of the function call
        
        Raises:
            Exception if max retries are reached
        """
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except litellm.RateLimitError as e:
                # Calculate wait time with exponential backoff
                wait_time = min(10 * (2 ** attempt), 120)  # Max wait time of 120 seconds
                
                print(f"Rate limit error detected. Attempt {attempt + 1}/{self.max_retries}")
                print(f"Error details: {e}")
                print(f"Waiting {wait_time:.2f} seconds before retrying...")
                
                time.sleep(wait_time)
            
            except Exception as e:
                # For non-rate-limit errors, raise immediately
                print(f"Unexpected error occurred: {e}")
                raise
        
        raise Exception(f"Failed to execute after {self.max_retries} attempts due to rate limiting")

    def create_crew(self) -> Crew:
        """
        Creates and returns a Crew object.

        Returns:
            Crew: The created Crew object, or None if an error occurred.
        """
        try:
            tasks = self._create_tasks()
            agents = self._create_agents()
            
            if not tasks:
                print("🚨 Error: Task creation failed.")
            if not agents:
                print("🚨 Error: Agent creation failed.")
            
            if not tasks or not agents:
                return None

            print(f"✅ Tasks Created: {tasks}")
            print(f"✅ Agents Created: {agents}")

            return self._retry_with_backoff(
                Crew,
                name="SEOCrew",
                tasks=tasks,
                agents=agents,
                process=Process.sequential,
                verbose=True
            )
    
        except Exception as e:
            print(f"Error creating crew: {e}")
            return None