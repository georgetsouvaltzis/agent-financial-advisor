from dotenv import load_dotenv
import asyncio
load_dotenv()

from application.shared_state import SharedState
from langchain_core.messages import HumanMessage, AIMessageChunk
from application.workflow.graph import create_workflow_graph
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

async def main():
    graph = create_workflow_graph()
    config = RunnableConfig(configurable={"thread_id": 1})
    human_message = [HumanMessage("I want to pruchase a house.")]
    state = SharedState(messages=human_message)

    await graph.ainvoke(state, config)

    while True:
        interrupts = graph.get_state(config).interrupts
        if interrupts:
            user_response = input(f"{interrupts[0].value}: ")
            async for token, metadata in graph.astream(Command(resume=user_response), config=config, stream_mode="messages"):
                if metadata["langgraph_node"] == "summarize" and isinstance(token, AIMessageChunk):
                    print(token.content, end="")
        else:
            break

if __name__ == "__main__":
    asyncio.run(main())