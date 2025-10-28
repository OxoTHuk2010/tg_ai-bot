from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from storage import PERSONS

def start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🎲 Интересный факт', callback_data='ramdom_fact')],
        [InlineKeyboardButton(text='👥 Общение с личностью', callback_data='person_talk')],
        [InlineKeyboardButton(text='🧠 Квиз', callback_data='quiz')],
        [InlineKeyboardButton(text='🌏 Переводчик', callback_data='translate')],
        [InlineKeyboardButton(text='🎥 Рекомендации', callback_data='recommendations')],
        [InlineKeyboardButton(text='💼 Помощь с резюме', callback_data='resume')],
    ])

def fact_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🎲 Хочу ещё факт', callback_data='ramdom_fact')],
        [InlineKeyboardButton(text='Закончить', callback_data="close_to_start")],
    ])

def get_persons_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=name, callback_data=f'persona:{name}')] for name in PERSONS]
        )


def close_mode():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Закончить', callback_data='close_to_start')]
    ])

def get_qviz_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='История', callback_data='topic:history')],
        [InlineKeyboardButton(text='Наука', callback_data='topic:science')],
        [InlineKeyboardButton(text='IT', callback_data='topic:it')],
        [InlineKeyboardButton(text='Кино', callback_data='topic:cinema')],
        [InlineKeyboardButton(text='Книги', callback_data='topic:book')],
    ])

def quiz_answers():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Ещё вопрос по теме', callback_data='next_question')],
        [InlineKeyboardButton(text='Смена темы', callback_data='change_topic')],
        [InlineKeyboardButton(text='Закончить игру', callback_data='end_quiz')],
    ])

def translate_lang_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Английский", callback_data="lang:английский")],
        [InlineKeyboardButton(text="Немецкий", callback_data="lang:немецкий")],
        [InlineKeyboardButton(text="Французский", callback_data="lang:французский")],
        [InlineKeyboardButton(text="Испанский", callback_data="lang:испанский")],
        [InlineKeyboardButton(text="Русский", callback_data="lang:русский")],
    ])

def translate_action_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сменить язык", callback_data="translate_change_lang")],
        [InlineKeyboardButton(text="Закончить", callback_data="close_to_start")],
    ])

def reco_category_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Фильмы", callback_data="reco_cat:films")],
        [InlineKeyboardButton(text="Книги", callback_data="reco_cat:books")],
        [InlineKeyboardButton(text="Музыка", callback_data="reco_cat:music")],
    ])

def reco_items_keyboard(items):
    """
    items: список dict с ключом 'title'. Кнопки "👎 1. <сокр.название>"
    callback_data: 'reco_dislike:<idx>'
    """
    rows = []
    for i, item in enumerate(items, 1):
        title = item.get("title", f"#{i}")
        short = (title[:28] + "…") if len(title) > 29 else title
        rows.append([InlineKeyboardButton(text=f"👎 {i}. {short}", callback_data=f"reco_dislike:{i}")])
    rows.append([InlineKeyboardButton(text="Закончить", callback_data="close_to_start")])
    return InlineKeyboardMarkup(inline_keyboard=rows)