from aiogram.fsm.state import State, StatesGroup

class MessageTalks(StatesGroup):
    message = State()