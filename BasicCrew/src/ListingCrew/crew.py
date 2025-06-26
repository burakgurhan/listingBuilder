# src/research_crew/crew.py
from typing import List
from crewai_tools import SerperDevTool
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from tools.custom_tools import validate_product_info, validate_writing_output
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import os 

groq_api_key = os.environ.get("GROQ_API_KEY")

@CrewBase
class ListingCrew():
    """Research crew for comprehensive topic analysis and reporting"""

    agents: List[BaseAgent]
    tasks: List[Task]

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
                api_key=groq_api_key,
                model_name=model_name,   #"mixtral-8x7b-32768",
                temperature=temperature,
            )
        except Exception as e:
            raise RuntimeError(f"Error initializing LLM: {e}")

    @agent
    def scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['scraper'], # type: ignore[index]
            verbose=True,
            max_retry_limit=3,
            tools=[SerperDevTool()],
            llm=self._create_llm(temperature=0.1), # type: ignore[index]
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
            tools=[SerperDevTool()],
            llm=self._create_llm(temperature=0.1), # type: ignore[index]
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'], # type: ignore[index]
            verbose=True,
            reasoning=True,
            max_reasoning_attemts=2,
            max_iter=5,
            llm=self._create_llm(temperature=0.1), # type: ignore[index]
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

    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )