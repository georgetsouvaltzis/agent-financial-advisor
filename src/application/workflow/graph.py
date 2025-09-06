from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import InMemorySaver

from application.shared_state import SharedState
from application.workflow.edges import should_ask_to_clarify
from application.workflow.nodes import ask_user_to_clarify, check_risk, collect_user_profile, plan_action, recommend_investment, summarize

def create_workflow_graph() -> CompiledStateGraph:
    builder = StateGraph(SharedState)
    builder.add_node(collect_user_profile)
    builder.add_node(ask_user_to_clarify)
    builder.add_node(check_risk)
    builder.add_node(recommend_investment)
    builder.add_node(plan_action)
    builder.add_node(summarize)

    builder.set_entry_point("collect_user_profile")
    builder.add_conditional_edges("collect_user_profile", should_ask_to_clarify)
    builder.add_edge("check_risk", "recommend_investment")
    builder.add_edge("recommend_investment", "plan_action")
    builder.add_edge("plan_action", "summarize")
    builder.set_finish_point("summarize")

    graph = builder.compile(checkpointer=InMemorySaver())
    return graph