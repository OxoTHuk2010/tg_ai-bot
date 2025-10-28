from openai import AsyncOpenAI
from config import OpenAI_KEY

client = AsyncOpenAI(api_key=OpenAI_KEY)

async def translate_text(lang: str, text: str) -> str:
    """
    lang: ru/en/de/fr/it/...
    """
    resp = await client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "system", "content": f"Ты профессиональный переводчик. Переведи на язык: {lang}. Кратко и точно"},
            {"role": "user", "content": text},
        ],
        temperature=0.2,
        max_tokens=600,
    )
    return resp.choices[0].message.content