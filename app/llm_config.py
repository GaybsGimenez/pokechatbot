import os
import openai
from dotenv import load_dotenv

load_dotenv()


LLM_CONFIG = {
    "model": "gpt-3.5-turbo",
    "temperature": 0,
    "top_p": 1,
    "max_tokens": 100,
}

openai.api_key = os.getenv("OPENAI_API_KEY")
