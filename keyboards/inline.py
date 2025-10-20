from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_keyboard():
    kb_list = [
        [InlineKeyboardButton(text='🎲 Интересный факт', callback_data='ramdom_fact')],
        [InlineKeyboardButton(text='👥 Общение с личностью', callback_data='toll_person')],
        [InlineKeyboardButton(text='🧠 Квиз', callback_data='qviz')],
        [InlineKeyboardButton(text='🌏 Переводчик', callback_data='translate')],
        [InlineKeyboardButton(text='🎥 Рекомендации', callback_data='recomendation')],
        [InlineKeyboardButton(text='💼 Помощь с резюме', callback_data='resume')],

    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def fact_again_keyboard():
    kb = [
        [InlineKeyboardButton(text='🎲 Интересный факт', callback_data='ramdom_fact')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard