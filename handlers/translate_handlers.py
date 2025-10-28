from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline import translate_lang_keyboard, translate_action_keyboard
from services.translate_service import translate_text
from states import TranslateStates

router = Router()

@router.callback_query(F.data == "translate")
async def translate_entry(call: CallbackQuery, state: FSMContext):
    await state.set_state(TranslateStates.choosing_lang)
    await call.message.answer("Выберите язык перевода:", reply_markup=translate_lang_keyboard())
    await call.answer()

@router.callback_query(F.data.startswith("lang:"))
async def translate_set_lang(call: CallbackQuery, state: FSMContext):
    lang = call.data.split(":")[-1]
    await state.update_data(lang=lang)
    await state.set_state(TranslateStates.waiting_text)
    await call.message.answer(f"Язык установлен: {lang}. Введите текст для перевода.")
    await call.answer()

@router.callback_query(F.data == "translate_change_lang")
async def translate_change_lang(call: CallbackQuery, state: FSMContext):
    await state.set_state(TranslateStates.choosing_lang)
    await call.message.answer("Выберите язык:", reply_markup=translate_lang_keyboard())
    await call.answer()

@router.message(TranslateStates.waiting_text)
async def translate_do(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "русский")
    res = await translate_text(lang, message.text)
    await message.answer(res, reply_markup=translate_action_keyboard())