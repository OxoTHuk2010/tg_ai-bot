from openai import OpenAI
from config import OpenAI_KEY
client = OpenAI(api_key=OpenAI_KEY)

async def get_fact():
    response = client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': 'Ты полезный помощник, который знает факты'},
            {'role': 'user', 'content': 'Верни интересный факт!'}
        ]
    )
    return response.choices[0].message.content
