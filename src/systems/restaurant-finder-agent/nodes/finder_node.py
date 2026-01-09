from ..config import Config
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from ..agent_state import AgentState

from tools.tavily_web_search import tavily_web_search

def finder_node(state:AgentState) -> AgentState:
    config = Config()    
    
    model = ChatOpenAI(
        openai_api_key=config.openai_api_key,
        model=config.openai_model_name,
        temperature=0.9,
        max_tokens=1000
    )

    model_with_tool = model.bind_tools([tavily_web_search])

    system_message = SystemMessage(
        content = "You are a highly skilled tourist guide in Melbourne Australia. " \
        "Use the Tavily web search tool to get the most recent information about restaurants in Melbourne, Australia."
    )
    
    human_message = HumanMessage(
        content=state["user_query"]
    )

    response = model_with_tool.invoke([
        system_message, 
        *state["messages"], 
        human_message
    ])   
    
    # print("Tool calls:", response.tool_calls)
    # print("LLM response", response)

    return {
        "messages": [response],
        "output_query": response.content
    }