import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
OpenAI_KEY = os.getenv('OPENAI_API_KEY')
