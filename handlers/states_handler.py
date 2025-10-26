from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from services.role_mode import ask_role_gpt
from keyboards.inline import close_mode
from states import MessageTalks
from storage import dialogues

router = Router()

@router.message(MessageTalks.message)
async def message_handler(message: Message):
    answer = await ask_role_gpt(message.from_user.id, message.text)
    persona = dialogues[message.from_user.id]['persona']
    await message.answer(f'Answer - {answer}', reply_markup=close_mode())