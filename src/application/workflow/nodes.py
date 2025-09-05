import json
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from pydantic import ValidationError
from typing import Literal
from src.application.agents.profile_agent import ProfileAgent
from src.application.shared_state import SharedState
from src.application.utils import extract_content_from_tags
from src.domain.user_profile import UserProfile
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


def collect_user_profile(state: SharedState) -> SharedState:
    return profile_agent.run(state)


def ask_user_to_clarify(state: SharedState) -> Command[Literal["collect_user_profile"]]:
    user_response = interrupt(f"\n{state.question_to_ask}")

    return Command(goto="collect_user_profile", update={"messages": [AIMessage(state.question_to_ask), HumanMessage(user_response)]})



def check_risk(state: SharedState) -> SharedState:
    return risk_agent.run(state)

def recommend_investment(state: SharedState) -> SharedState:
    return investment_agent.run(state)

def plan_action(state: SharedState) -> SharedState:
    return plan_agent.run(state)

def summarize(state: SharedState) -> SharedState:
    return summarizer_agent.run(state)