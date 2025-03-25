import time
import litellm
from crewai import Crew
from crewai import Process
from agents.scraper_agent import ScraperAgent
from agents.researcher_agent import ResearcherAgent
from agents.editor_agent import EditorAgent
from tasks.scraping_task import ScrapingTask
from tasks.research_task import ResearchTask
from tasks.writing_task import WritingTask

class SEOCrew:
    """A crew responsible for SEO-related tasks including scraping, research, and content writing."""
    def __init__(self, url, max_retries=3):
        """Initialize the SEO Crew with a target URL.
        
        Args:
            url (str): The target URL for SEO operations. Must be a valid HTTP/HTTPS URL.
        """
        self.url = url
        self.max_retries = max_retries
    def _create_tasks(self):
        return [
            ScrapingTask(self.url).create_scraping_task(),
            ResearchTask().create_research_task(),
            WritingTask().create_writing_task()
        ]

    def _create_agents(self):
        return [
            ScraperAgent().create_scraper_agent(),
            ResearcherAgent().create_researcher_agent(),
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
                wait_time = (5 ** attempt) + (attempt * 0.5)
                
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
            # Use the retry mechanism when creating the crew
            return self._retry_with_backoff(
                Crew,
                name="SEOCrew",
                tasks=self._create_tasks(),
                agents=self._create_agents(),
                process=Process.sequential,
                verbose=True
            )
        
        except Exception as e:
            print(f"Error creating SEOCrew: {e}")
            return None
