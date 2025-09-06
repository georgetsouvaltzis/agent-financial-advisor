from typing import Annotated
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages, MessagesState
from langchain_core.messages import AnyMessage

from domain.user_profile import UserProfile

class SharedState(MessagesState):
    user_profile: UserProfile
    question_to_ask: str
    user_response: str
    risk_report: str
    risk_flags: list[str]
    disposable_income: int | float
    recommender_agent_summary: dict
    action_plan_agent_summary: dict

    # user_profile: UserProfile = Field(default=None, description="contains information regarding User's income/expenses/their risk tolerance etc.")
    # question_to_ask: str | None = Field(default=None, description="question provided by LLM to ask user for clarification purposes.")
    # user_response: str | None = Field(default=None, description="User's provided response for the question that has been asked by LLM.")
    # risk_report: str = Field(default=None)
    # risk_flags: list[str] = Field(default=[])

    # disposable_income: int | float = Field(default=0, description="Calculated disposable income based on user's provided details")

    # recommender_agent_summary: dict = Field(default={})

    # action_plan_agent_summary: dict = Field(default={})

