
from storage import dialogues,PERSONS
from openai import AsyncOpenAI
from config import OpenAI_KEY

client = AsyncOpenAI(api_key=OpenAI_KEY)

async def ask_role_gpt(user_id: int, text: str) -> str:
    print(dialogues[user_id])

    if user_id not in dialogues:
        return 'Сначала начните диалог командой /talk'

    dialogues[user_id]['messages'].append({'role': 'user', 'content': text})
    persona = dialogues[user_id]['persona']

    response = await client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': f'Ты общаешься как персона: {persona}. Никогда не выходи из этой роли'},
            *dialogues[user_id]['messages'],
        ],
        temperature=0.7,
        max_tokens=400
    )

    answer = response.choices[0].message.content
    dialogues[user_id]['messages'].append({'role': 'assistant', 'content': answer})

    return answer