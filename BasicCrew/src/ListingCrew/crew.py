# src/research_crew/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from tools.custom_tools import validate_product_info

@CrewBase
class ListingCrew():
    """Research crew for comprehensive topic analysis and reporting"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['scraper'], # type: ignore[index]
            verbose=True,
            max_retry_limit=3,
            tools=[SerperDevTool()]
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
            tools=[SerperDevTool()]
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'], # type: ignore[index]
            verbose=True,
            reasoning=True,
            max_reasoning_attemts=2,
            max_iter=5
        )

    @task
    def scraping_task(self) -> Task:
        return Task(
            config=self.tasks_config['scraping_task'], # type: ignore[index]
            guardrail=validate_product_info, # type: ignore[arg-type]
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
            #output_file='output/report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )