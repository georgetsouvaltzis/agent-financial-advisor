from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from typing import Literal
from application.agents.profile_agent import ProfileAgent
from application.shared_state import SharedState
from ..agents.investment_agent import InvestmentAgent
from ..agents.plan_agent import PlanAgent
from ..agents.risk_agent import RiskCheckAgent
from ..agents.summarizer_agent import SummarizerAgent
from langgraph.types import Command, interrupt


risk_agent = RiskCheckAgent()
investment_agent = InvestmentAgent()
plan_agent = PlanAgent()
summarizer_agent = SummarizerAgent()
profile_agent = ProfileAgent()


async def collect_user_profile(state: SharedState) -> SharedState:
    return await profile_agent.run(state)

async def check_risk(state: SharedState) -> SharedState:
    return await risk_agent.run(state)

async def recommend_investment(state: SharedState) -> SharedState:
    return await investment_agent.run(state)

async def plan_action(state: SharedState) -> SharedState:
    return await plan_agent.run(state)

async def summarize(state: SharedState) -> SharedState:
    return await summarizer_agent.run(state)

def ask_user_to_clarify(state: SharedState) -> Command[Literal["collect_user_profile"]]:
    user_response = interrupt(f"\n{state["question_to_ask"]}")

    return Command(goto="collect_user_profile", update={"messages": [AIMessage(state["question_to_ask"]), HumanMessage(user_response)]})
