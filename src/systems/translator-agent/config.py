import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        
        self._openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self._openai_api_key:
            raise EnvironmentError("OPENAI_API_KEY not set.")
        
        self._openai_model_name = os.getenv("OPENAI_MODEL_NAME")
        if not self._openai_model_name:
            raise EnvironmentError("OPENAI_MODEL_NAME not set.")


    @property
    def openai_api_key(self):
        return self._openai_api_key

    @property
    def openai_model_name(self):
        return self._openai_model_name
