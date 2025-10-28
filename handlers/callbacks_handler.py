from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from services.quiz_manager import init_quiz
from services.random_fact import get_fact
from services.quiz_service import get_quiz_question
from keyboards.inline import fact_keyboard, get_persons_keyboard, get_qviz_keyboard, start_keyboard
from storage import dialogues, PERSONS
from states import MessageTalks, QuizStates

router = Router()

# === RANDOM FACT ===
@router.callback_query(F.data == 'ramdom_fact')
async def random_handler(call: CallbackQuery):
    await call.answer()
    await call.message.answer("Случайный факт:")
    fact = await get_fact()
    await call.message.answer(f'{fact}', reply_markup=fact_keyboard())

# === TALK ===
@router.callback_query(F.data == 'person_talk')
async def person_talk_handler(call: CallbackQuery):
    await call.answer()
    await call.message.answer('Выберите личность:', reply_markup=get_persons_keyboard())

@router.callback_query(F.data.startswith('persona:'))
async def persona_handler(call: CallbackQuery, state: FSMContext):
    persona = call.data.split(':')[-1]

    #Инициализируем историю
    dialogues[call.from_user.id] = {
        'persona': PERSONS[persona],
        'messages': []
    }
    await call.answer()
    await call.message.answer(f'Вы выбрали {persona}. Можете писать сообщения')
    await state.set_state(MessageTalks.message)

# === CLOSE -> START ===
@router.callback_query(F.data == 'close_to_start')
async def close_to_start_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await call.message.edit_reply_markup(reply_markup=None)
    except TelegramBadRequest:
        pass
    await call.message.answer("Главное меню:", reply_markup=start_keyboard())
    await call.answer("Возврат в меню")

# === QUIZ ===
@router.callback_query(F.data == 'quiz')
async def quiz_handler(call: CallbackQuery, state: FSMContext):
    await init_quiz(state)
    await state.set_state(QuizStates.choosing_topic)
    await call.answer()
    await call.message.answer('Выберите тему Квиза:', reply_markup=get_qviz_keyboard())

@router.callback_query(F.data.startswith('topic:'))
async def quiz_question_handler(call: CallbackQuery, state: FSMContext):
    await call.answer("Подготовка вопроса...", show_alert=False)
    topic = call.data.split(':')[-1]
    data = await state.get_data()
    asked = data.get("asked_questions", [])
    question = await get_quiz_question(topic, asked)
    asked.append(question)
    await state.update_data(question=question, topic=topic, asked_questions=asked)
    await state.set_state(QuizStates.waiting_answer)
    await call.message.answer(f'Тема: {topic}\n\n{question}\n\nВведи свой ответ.')