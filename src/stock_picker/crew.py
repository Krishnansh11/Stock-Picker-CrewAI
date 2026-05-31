from crewai import Agent, Crew, Process, Task, LLM
from crewai import memory
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List
from .tools.push_tool import TelegramNotificationTool
# from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
# from crewai.memory.storage.rag_storage import RAGStorage
# from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
# Long Term Memory

class TrendingCompany(BaseModel):
    """ A company that is in the news and attracting attention """
    name: str=Field(description="Company name"),
    ticker: str=Field(description="Stock Ticker Symbol"),
    reason: str=Field(description="reason this company is trending in the news")

class TrendingCompanyList(BaseModel):
    """ List of all the trending companies that are in the news"""
    companies: List[TrendingCompany]=Field(description="List of trending companies that are in the news")

class TrendingCompanyResearch(BaseModel):
    """ Detailed research on a company"""
    name: str=Field(description="Company name")
    market_population: str=Field(description="Current market position and competitive analysis")
    future_outlook: str=Field(description="Future outlook and growth perspective")
    investment_potential: str=Field(description="Investment potential and suitability for investment")

class TrendingCompanyResearchList(BaseModel):
    """ List of all the trending companies that are in the news"""
    research_list: List[TrendingCompanyResearch]=Field(description="Comprehensive research on all trending companies")

@CrewBase
class StockPicker():
    """StockPicker crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def trending_comapny_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['trending_comapny_finder'],tools=[SerperDevTool()] 
            ,verbose=True,
            memory=True
        )

    @agent
    def financial_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_researcher'],tools=[SerperDevTool()] # type: ignore[index]
            ,verbose=True
        )

    @agent
    def stock_picker(self) -> Agent:
        return Agent(
            config=self.agents_config['stock_picker'],# type: ignore[index]
            verbose=True,
            tools=[TelegramNotificationTool()],
            memory=True
        )
        
    # @agent
    # def manager(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['manager'], # type: ignore[index]
    #         verbose=True
    #     )

    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['find_trending_companies'], # type: ignore[index]
            output_pydantic=TrendingCompanyList
        )

    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['research_trending_companies'] # type: ignore[index]
            ,output_pydantic=TrendingCompanyResearchList
        )

    @task
    def pick_best_company(self) -> Task:
        return Task(**self.tasks_config['pick_best_company']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the StockPicker crew"""
        manager = Agent(
            config= self.agents_config['manager'],
            allow_delegation = True, # equilent to handoffs in openAi SDK,
            llm = "google/gemini-2.0-flash"
        )


        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            verbose=True,
            process=Process.hierarchical,
            manager_agent=manager
            # short_term_memory=short_term_memory,
            # long_term_memory=long_term_memory,
            # entity_memory=entity_memory
        )
