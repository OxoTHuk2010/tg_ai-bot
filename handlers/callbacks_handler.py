from aiogram import F, Router
from aiogram.types import CallbackQuery
from services.random_fact import get_fact
from keyboards.inline import fact_again_keyboard


router = Router()

@router.callback_query(F.data == 'ramdom_fact')
async def random_handler(call: CallbackQuery):
    await call.answer("Сейчас будет предоставлен случайный факт ", show_alert=True)
    fact = await get_fact()
    await call.message.answer(f'{fact}', reply_markup=fact_again_keyboard())
