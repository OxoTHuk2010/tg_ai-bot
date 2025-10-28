from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from storage import PERSONS

def start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🎲 Интересный факт', callback_data='ramdom_fact')],
        [InlineKeyboardButton(text='👥 Общение с личностью', callback_data='person_talk')],
        [InlineKeyboardButton(text='🧠 Квиз', callback_data='quiz')],
        [InlineKeyboardButton(text='🌏 Переводчик', callback_data='translate')],
        [InlineKeyboardButton(text='🎥 Рекомендации', callback_data='recommendation')],
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
