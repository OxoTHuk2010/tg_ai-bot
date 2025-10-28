from openai import AsyncOpenAI
from config import OpenAI_KEY

client = AsyncOpenAI(api_key=OpenAI_KEY)

async def get_quiz_question(topic:str, asked: list[str] | None = None) -> str:
    aboid_block = ""
    if asked:
        avoid_joined = " | ".join(asked[-15:])
        aboid_block = f"\nНе повторяй вопросы из списка (если есть совпадение по смыслу - сформулируй новый): {avoid_joined}"

    resp = await client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{
            'role': 'system',
            'content': (
                f'Сгенерируй один вопрос для квиза по теме "{topic}".'
                f'Верни только вопрос на русском, без ответа и пояснений.'
                + aboid_block
            )
        }],
        temperature=0.7,
        max_tokens=200,
    )
    return resp.choices[0].message.content.strip()

async def check_answer(question: str, answer: str) -> str:
    resp = await client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                'role': 'system',
                'content': (
                    f"Проверь правильность ответа на квиз.\n"
                    f"Вопрос: {question}\n"
                    f"Ответ: {answer}\n"
                    'Скажи только одно слово: "правильно" или "неправильно".'
                ),
            }
        ],
        temperature=0,
        max_tokens=10,
    )
    return resp.choices[0].message.content.strip().lower()