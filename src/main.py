from dotenv import load_dotenv
load_dotenv()

from application.shared_state import SharedState
from langchain_core.messages import HumanMessage
from application.workflow.graph import create_workflow_graph
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command


def main():
    graph = create_workflow_graph()

    config = RunnableConfig(configurable={"thread_id": 1})

    human_message = [HumanMessage("I want to purchase a house. I'm making 3k a month and spending 2k a month. I want to have low risk preference and I want to save 50,000$")]

    human_message = [HumanMessage("I want to pruchase a house.")]
    state = SharedState(messages=human_message)
    res = graph.invoke(state, config)
    print(res)

    while True:
        interrupts = graph.get_state(config).interrupts
        if interrupts:
            user_response = input(interrupts[0].value)
            graph.invoke(Command(resume=user_response), config)
        else:
            break

if __name__ == "__main__":
    main()