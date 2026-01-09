import json
from .tool_config import ToolConfig
from tavily import TavilyClient
from langchain_core.tools import tool

@tool
def tavily_web_search(query):
    """ Performs web serch based on user query using Tavily API."""
    config = ToolConfig()  
    
    tavily_client = TavilyClient(api_key=config.tavily_api_key)
    
    response = tavily_client.search(query)
    
    json_response =  json.dumps(response, indent=2)

    # print("Tavily Web Search Response:", json_response)
    
    return json_response
