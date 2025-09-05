import json
from pydantic import ValidationError
from langchain_core.messages import HumanMessage, SystemMessage
from src.application.agents.base_agent import BaseAgent
from src.application.shared_state import SharedState
from src.application.utils import extract_content_from_tags
from src.domain.user_profile import UserProfile


class ProfileAgent(BaseAgent):
    def run(self, state: SharedState) -> SharedState:
        prompt_template = """
    You are a financial assistant. Your task is to extract a user's financial profile from their message, strictlyt following the provided JSON schema.

    Instructions:
    1. Use the JSON schema provided in <schema></schema> as an example to determine which fields to extract, their types, and any default values.
    2. If a field is missing in the user's input but has a default in the schema use that default.
        - If the field is mandatory and missing, Generate a short descriptive question and (if mthere are multiple questions to ask, unify and ask as single) and enclose it within <question_to_ask></question_to_ask>

    3. only include fields defined in the schema.
    4. output valid JSON
    5. Do not add any extra fields
    6. Do not make any assumptions. Strictly follow the guidelines

    <schema>
    %s
    </schema>

    This is the input example:
    "I earn 5000$ per month and I spend 3000$. I want to save 2000$ for a vacation."

    Example of expected JSON output(wrap the JSON within <generated_json></generated_json> tags):
    {
        "income": 5000,
        "expenses": 3000,
        "tolerance": "medium",
        "preferences": [],
        "goals: [{"name": "vacation", "amount": 2000}]
    }
    """
        system_message = SystemMessage(prompt_template % UserProfile.get_json_schema())

        try:
            llm_response = self._llm.invoke([system_message] + state.messages)
            extracted_content = extract_content_from_tags("question_to_ask", llm_response.content)
            if extracted_content is not None:
                return SharedState(**state, messages=[] + [llm_response], question_to_ask=extracted_content)

            extracted_content = extract_content_from_tags("generated_json", llm_response.content)

            extracted_json = json.loads(extracted_content)

            user_profile = UserProfile(**extracted_json)
        
        except ValidationError as e:
            print("validation error!")
            user_profile = None
        
        return SharedState(**state, question_to_ask=None, user_response=None, messages=[llm_response], user_profile=user_profile)
            

