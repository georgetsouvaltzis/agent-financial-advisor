from pydantic import Field, BaseModel


class Goal(BaseModel):
    name: str = Field(description="Name of the goal that user is trying to achieve")
    amount: float = Field(description="Amount that user is trying to save for the given goal")