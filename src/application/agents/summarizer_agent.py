import json
from application.agents.base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage

from application.shared_state import SharedState

class SummarizerAgent(BaseAgent):
    async def run(self, state: SharedState) -> SharedState:
        system_message = SystemMessage("""
        You are a professional financial assistant. Your task is to summarize a user's complete financial profile, risk assessment, investment recommendations, and action plan into a single, coherent report in plain, human-friendly language.
        You will receive:
        1. The user's profile (income, expenses, risk tolerance, goals, preferences)
        2. Risk assessment details(risk report, risk flags, disposable income)
        3. Inveastment recmomendations (ivnestment plan and summary)
        4. Action plan (action steps and summary)


        Instructions:
        - Generate a single narrative that covers all sections:
            1. Profile Overview
            2. Risk analysis
            3. Investment recommendations
            4. Action Plan

        - Keep it clear, concise and easy to understand for someone without financial expertise.
        - Highlight important points and actionable insights.
        - Do not add extra information beyond what's provded in the input.
        - Maintain a supportive and professional tone.
        """) 

        llm_input = {
            "profile": state["user_profile"].model_dump(),
            "risk_report": state["risk_report"],
            "risk_flags": state["risk_flags"],
            "disposable_income": state["disposable_income"],
            "investment_plan": json.dumps(state["recommender_agent_summary"]),
            "action_steps_and_summary": json.dumps(state["action_plan_agent_summary"])
        }    

        human_message = HumanMessage(json.dumps(llm_input))

        res = await self._llm.ainvoke([system_message, human_message])

        return {
            "messages": [res]
        }

        

