
from application.shared_state import SharedState
from typing import Literal

def should_ask_to_clarify(state: SharedState) -> Literal["ask_user_to_clarify", "check_risk"]:
    user_profile = state.get("user_profile", None)

    if user_profile is None or user_profile.income == 0 or user_profile.expenses == 0:
        return "ask_user_to_clarify"
    
    return "check_risk"