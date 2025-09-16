import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
LLM_API_KEY = os.getenv("API_KEY")
LLM_ENDPOINT = os.getenv("ENDPOINT")
LLM_MODEL = os.getenv("MODEL")