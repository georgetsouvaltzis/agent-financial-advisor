import json
from application.agents.base_agent import BaseAgent
from application.shared_state import SharedState
from langchain_core.messages import SystemMessage, HumanMessage

class InvestmentAgent(BaseAgent):
    async def run(self, state: SharedState) -> SharedState:
        system_prompt = SystemMessage("""
        You are a professional financial advisor. Your job is to create an investment strategy for a user based on their financial profile and risk assessment.
        1. You will receive user's profile(income, monthly expenses, risk tolerance, goals, preferences)
        2. Calculation of (disposable income, risk flags and report)

        Instructions:
        - Only suggest investmets that match the user's risk tolerance and financial situation.
        - If disposable income is very low or negative, advise to increase savings before investing.
        - Align suggested investments with the user's goals. (short-term vs long-term)


        This is the JSON format of the output.: 
        {
            "recommendations": [
            "type": "<risk category or goal alignment>",
            "options": ["<investment options>"],
            "reasoning": "<brief explanation>"
            ],
            "investment_summary": "<user facing summary in plain english loanguage>"
        }

        
        Things to keep in mind:
        - Use realistic investment options (stocks, ETFs, bonds, saving accounts, crypto and others)
        - Provide a short reasoning for each recommendation.
        - Maintain a supportive and educational tone.
        - Do not invent any kind of number. Rely only on the provided user profile and calculations.
        - Keep JSON strictly valid without adding any extra fields.
        - Output plain JSON without anything additional
        """)

        llm_input = {
            "profile": state["user_profile"].model_dump(),
            "risk_assesment": {
                "disposable_income": state["disposable_income"],
                "risk_flags": state["risk_flags"],
                "risk_report": state["risk_report"]
            }
        }

        human_message = HumanMessage(json.dumps(llm_input))

        res = await self._llm.ainvoke([system_prompt, human_message])
        extracted_json = json.loads(res.content)
        return {
            "recommender_agent_summary": extracted_json
        }


