import os
from dotenv import load_dotenv

class ToolConfig:
    def __init__(self):
        load_dotenv()
        
        self._tavily_api_key = os.getenv("TAVILY_API_KEY")
        if not self._tavily_api_key:
            raise EnvironmentError("TAVILY_API_KEY not set.")

    @property
    def tavily_api_key(self):
        return self._tavily_api_key