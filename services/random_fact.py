from openai import AsyncOpenAI
from config import OpenAI_KEY

client = AsyncOpenAI(api_key=OpenAI_KEY)

async def get_fact() -> str:
    response = await client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': 'Ты полезный помощник, который знает факты.'},
            {'role': 'user', 'content': 'Верни один небанальный факт на русском.'},
        ],
        temperature=0.7,
        max_tokens=200,
    )
    return response.choices[0].message.content
