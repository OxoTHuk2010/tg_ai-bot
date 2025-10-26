from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from services.random_fact import get_fact
from keyboards.inline import fact_again_keyboard, get_persons_keyboard
from storage import dialogues, PERSONS
from states import MessageTalks

router = Router()

@router.callback_query(F.data == 'ramdom_fact')
async def random_handler(call: CallbackQuery):
    await call.answer("Сейчас будет предоставлен случайный факт ", show_alert=True)
    fact = await get_fact()
    await call.message.answer(f'{fact}', reply_markup=fact_again_keyboard())

@router.callback_query(F.data == 'person_tolk')
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
    print(dialogues)
    await call.message.answer(f'Вы выбрали {persona}. Можете пообщаться с ним')
    await call.answer()
    await state.set_state(MessageTalks.message)

@router.callback_query(F.data == 'close_mode')
async def close_mode_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await call.message.edit_text("Диалог завершён", reply_markup=None)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            await call.message.delete()
            raise

    await call.answer("Диалог завершён", show_alert=True)