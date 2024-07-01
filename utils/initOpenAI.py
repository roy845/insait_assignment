from openai import OpenAI
from config import settings

def init_open_ai_client():
    client = OpenAI(
        api_key=settings.openai_api_key
    )
   

    return client