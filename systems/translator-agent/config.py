import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self._openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self._openai_api_key:
            raise EnvironmentError(
                "OPENAI_API_KEY not set. Please check your .env file or environment variables."
            )

    @property
    def openai_api_key(self):
        return self._openai_api_key
