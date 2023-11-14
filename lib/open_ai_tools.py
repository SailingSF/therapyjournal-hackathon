from openai import OpenAI
from os import getenv
from dotenv import load_dotenv

load_dotenv()


def get_open_ai_client():
    return OpenAI(api_key=getenv("OPENAI_API_KEY"))
