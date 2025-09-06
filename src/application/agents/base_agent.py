from abc import ABC, abstractmethod

from langchain_groq import ChatGroq

from application.shared_state import SharedState

class BaseAgent(ABC):
    """
    
    Abstract base class for all agents.
    Each agent must implement the run method that accepts and returns SharedState.
    """

    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        self._llm = ChatGroq(model=model_name)

    @abstractmethod
    async def run(self, state: SharedState) -> SharedState:
        pass

