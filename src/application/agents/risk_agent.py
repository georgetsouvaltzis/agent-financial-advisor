import json
from src.application.agents.base_agent import BaseAgent
from src.application.shared_state import SharedState
from langchain_core.messages import SystemMessage, HumanMessage


class RiskCheckAgent(BaseAgent):
    def run(self, state: SharedState) -> SharedState:
        system_message = SystemMessage("""
        You are a financial risk assessment assistant.
        Your task is to review a user's financial profile and explain potential risks and feasability of their financial situation.

        You will be provided with:
        1. The user's profile (income,  expenses, risk tolerance, goals, preferences).

        Instructions:
        - Carefully read the profile
        - Provide a concise but clear "Risk report" in plain English.
        - Explicitly explain why each risk flag matters in user-friendly terms
        - If the user's risk tolerance is misaligned with their financial reality highlight it
        - If goals are unrealistic suggest adjustments. (e.g. smaller goals, longer timeframe)
        - Maintain a supportive and professional tone
        - Do not invent numbers. Rely only on provided profile and calculations
        - Keep your output in under 150-200 words.""")
        
        profile = state.user_profile
        risk_flags = []
        disposable_income = profile.income - profile.expenses

        if disposable_income < 0:
            risk_flags.append("Negative cash flow")
        
        elif disposable_income < profile.income * 0.1:
            risk_flags.append("Low disposable income (<10% of income)")
        
        if profile.tolerance == "high" and disposable_income < profile.income * 0.1:
            risk_flags.append("High risk tolerance misaligned with limited finances")
        

        for goal in profile.goals:
            if goal.amount > disposable_income * 12: # TODO: currently hardcoded assuming that user wants to achieve within a year. Should be asked
                risk_flags.append(f"Goal: '{goal.name}' may be unrealistic with current savings")
            

        llm_input = {
            "profile": profile.model_dump(),
            "calculations": {
                "disposable_income": disposable_income,
                "risk_flags": risk_flags
            }
        }

        human_message = HumanMessage(json.dumps(llm_input))

        res = self._llm.invoke([system_message, human_message])
        
        return SharedState(**state, messages=[res], risk_report=res.content, risk_flags=risk_flags, disposable_income=disposable_income)
