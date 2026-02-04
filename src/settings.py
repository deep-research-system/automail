import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    openai_api = os.getenv("OPENAI_API_KEY")
    llm_model = "gpt-4o-mini"

settings = Settings()
