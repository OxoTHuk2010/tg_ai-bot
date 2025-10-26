from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from storage import PERSONS

def start_keyboard():
    kb_list = [
        [InlineKeyboardButton(text='🎲 Интересный факт', callback_data='ramdom_fact')],
        [InlineKeyboardButton(text='👥 Общение с личностью', callback_data='person_tolk')],
        [InlineKeyboardButton(text='🧠 Квиз', callback_data='qviz')],
        [InlineKeyboardButton(text='🌏 Переводчик', callback_data='translate')],
        [InlineKeyboardButton(text='🎥 Рекомендации', callback_data='recomendation')],
        [InlineKeyboardButton(text='💼 Помощь с резюме', callback_data='resume')],

    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def fact_again_keyboard():
    kb = [
        [InlineKeyboardButton(text='🎲 Хочу ещё факт', callback_data='ramdom_fact')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

def get_persons_keyboard():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data=f'persona:{name}')]
            for name in PERSONS
        ]
    )
    return kb

def close_mode():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Закончить', callback_data='close_mode')]
        ]
    )
    return kb