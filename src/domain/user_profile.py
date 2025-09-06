from pydantic import Field, BaseModel
from typing import Literal

from domain.goal import Goal


class UserProfile(BaseModel):
    income: float = Field(description="monthly income")
    expenses: float = Field(description="monthly expenses")
    tolerance: Literal["low", "medium", "high"] = Field(description="how risk tolerant user is.")
    goals: list[Goal] = Field(default=[], description="A list of goals that user is trying to achieve by investing")