import json
from openai import AsyncOpenAI
from config import OpenAI_KEY

client = AsyncOpenAI(api_key=OpenAI_KEY)

_SCHEMA = (
    'Ответ верни строго в JSON, без комментариев и преамбул, по схеме: '
    '{"item":[{"title": "<название>", "why": "<1-2 предложения описания>"}]}'
)

async def get_recommendations_structured(category: str, genre: str, blacklist: list[str]) -> list[dict]:
    bl = ", ".join(blacklist) if blacklist else "-"
    promt = (
        f"Категория: {category}\nЖанр: {genre}\n"
        f"Не предлагать: {bl}\n"
        f"Дай ровно 5 рекомендаций.\n{_SCHEMA}"
    )
    resp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты даёшь точные рекомендации по медиа на русском языке."},
            {"role": "user", "content": promt},
        ],
        temperature=0.7,
        max_tokens=900,
    )
    raw = resp.choices[0].message.content
    print(raw)
    try:
        data = json.loads(raw)
        item = data.get("items", [])

        norm = []
        for it in item[:5]:
            norm.append({
                "title": str(it.get("title","")).strip(),
                "why": str(it.get("why", "")).strip()
            })
        return [x for x in norm if x["title"]]
    except Exception:
        return []