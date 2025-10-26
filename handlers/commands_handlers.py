from aiogram import Router
from aiogram.types import Message
from aiogram.filters import  Command

from keyboards.inline import start_keyboard, get_persons_keyboard
from services.random_fact import get_fact

router = Router()

@router.message(Command('start'))
async def start_command(message: Message):
    await message.answer("Выберите интересуемый пункт: ", reply_markup=start_keyboard())

@router.message(Command('random'))
async def random_handler(message: Message):
    await message.answer("Сейчас будет предоставлен случайный факт")
    fact = await get_fact()
    await message.answer(f'{fact}')

@router.message(Command('talk'))
async def talk_handler(message: Message):
    await message.answer("Выберите личность с которой хотите пообщаться", reply_markup=get_persons_keyboard())