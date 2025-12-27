from config import Config
from langchain_openai import OpenAI

def translator_node(state:dict):
    config = Config()
    llm = OpenAI(
        openai_api_key=config.openai_api_key,
        temperature=0.9,
        max_tokens=100
    )
    
    response = llm.invoke(state["messages"])
    return {"messages": [response]}