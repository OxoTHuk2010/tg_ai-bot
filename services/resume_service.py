from openai import AsyncOpenAI
from config import OpenAI_KEY

client = AsyncOpenAI(api_key=OpenAI_KEY)

async def generate_resume(education: str, experience: str, skills: str) -> str:
    """
    :param education:
    :param experience:
    :param skills:
    :return: markdown-шаблон резюме.
    """
    resp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты HR-консультант. Собери компактное резюме в стиле markdown на русском."},
            {"role": "user", "content":
                f"Дай шаблон резюме по данным:\n"
                f"Образование: {education}\nОпыт: {experience}\nНавыки: {skills}\n"
                f"Структура: Заголовок с именем (пустое имя — оставить как «Имя Фамилия»), Контакты (заглушки),\n"
                f"Краткое summary (1-2 предложения), Опыт (пункты), Образование, Навыки (список), Дополнительно.\n"
                f"Без лишних комментариев — только итоговый markdown."
             },
        ],
        temperature=0.4,
        max_tokens=900,
    )
    return resp.choices[0].message.content