from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import  Command

from keyboards.inline import start_keyboard, get_persons_keyboard, get_qviz_keyboard
from services.quiz_manager import init_quiz
from services.random_fact import get_fact
from states import QuizStates

router = Router()

@router.message(Command('start'))
async def start_command(message: Message):
    await message.answer("Выберите интересуемый пункт: ", reply_markup=start_keyboard())

@router.message(Command('random'))
async def random_command(message: Message):
    await message.answer("Сейчас будет предоставлен случайный факт")
    fact = await get_fact()
    await message.answer(f'{fact}')

@router.message(Command('talk'))
async def talk_command(message: Message):
    await message.answer("Выберите личность с которой хотите пообщаться", reply_markup=get_persons_keyboard())

@router.message(Command('qviz'))
async def qviz_command(message: Message, state: FSMContext):
    await init_quiz(state)
    await state.set_state(QuizStates.choosing_topic)
    await message.answer("Выберите тему для вопроса: ", reply_markup=get_qviz_keyboard())