from aiogram.fsm.state import State, StatesGroup

#Диалог с личностью
class MessageTalks(StatesGroup):
    message = State()

#Квиз
class QuizStates(StatesGroup):
    choosing_topic = State()
    waiting_answer = State()

#Переводчик
class TranslateStates(StatesGroup):
    choosing_lang = State()
    waiting_text = State()

#Рекомендации
class RecoStates(StatesGroup):
    choosing_category = State()
    waiting_genre = State()