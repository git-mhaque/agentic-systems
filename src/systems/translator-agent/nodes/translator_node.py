from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from ..config import Config
from ..agent_state import AgentState

def translator_node(state:AgentState) -> AgentState:
    config = Config()    
    
    model = ChatOpenAI(
        openai_api_key=config.openai_api_key,
        model=config.openai_model_name,
        temperature=0.9,
        max_tokens=100
    )

    system_message = SystemMessage(content = "You are a highly skilled translator. Translate the user's message into French, maintaining the original meaning and tone.")
    human_message = HumanMessage(content=state["user_query"])

    response = model.invoke([system_message, *state["messages"], human_message])   
    return {"messages": [response],
            "output_query": response.content}