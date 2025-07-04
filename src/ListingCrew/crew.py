from typing import List
from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task # type: ignore
from crewai.agents.agent_builder.base_agent import BaseAgent
from tools.custom_tools import validate_product_info, validate_writing_output
from dotenv import load_dotenv
import time
import litellm
load_dotenv()

@CrewBase
class ListingCrew():
    """Research crew for comprehensive topic analysis and reporting"""

    agents: List[BaseAgent]
    max_retries: int = 3

    @agent
    def scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['scraper'], # type: ignore[index]
            verbose=True,
            max_retry_limit=3,
            tools=[WebsiteSearchTool(), ScrapeWebsiteTool()],
        )
    
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True,
            max_iter=10,
            reasoning=True,
            max_reasoning_attemts=2,
            respect_context_window=True,
            tools=[WebsiteSearchTool(), ScrapeWebsiteTool()],
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'], # type: ignore[index]
            verbose=True,
            reasoning=True,
            max_reasoning_attemts=2,
            max_iter=5,
        )

    @task
    def scraping_task(self) -> Task:
        return Task(
            config=self.tasks_config['scraping_task'], # type: ignore[index]
            #guardrail=validate_product_info, # type: ignore[arg-type]
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'] # type: ignore[index]
        )

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writing_task'], # type: ignore[index]
            max_retries=2,
            #guardrail=validate_writing_output
            #output_file='output/report.md'
        )

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

    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return self._retry_with_backoff(
            lambda: Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            )
        )