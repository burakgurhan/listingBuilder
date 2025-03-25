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
    def __init__(self, url):
        """Initialize the SEO Crew with a target URL.
        
        Args:
            url (str): The target URL for SEO operations. Must be a valid HTTP/HTTPS URL.
        """
        self.url = url

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

    def create_crew(self) -> Crew:
        """
        Creates and returns a Crew object.

        Returns:
            Crew: The created Crew object, or None if an error occurred.
        """
        try:
            return Crew(
                name="SEOCrew",
                tasks=self._create_tasks(),
                agents=self._create_agents(),
                process=Process.sequential,
                verbose=True
            )
        except Exception as e:
            print(f"Error creating SEOCrew: {e}")
            return None
