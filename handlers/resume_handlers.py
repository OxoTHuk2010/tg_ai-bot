from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from keyboards.inline import start_keyboard, close_mode
from services.resume_service import generate_resume
from states import ResumeStates

router = Router()

@router.callback_query(F.data == "resume")
async def resume_entry(call: CallbackQuery, state: FSMContext):
    await state.set_state(ResumeStates.collecting_education)
    await call.message.answer("Укажи ОБРАЗОВАНИЕ (ВУЗ, годы, спец.):")
    await call.answer()

@router.message(ResumeStates.collecting_education)
async def resume_education(message: Message, state: FSMContext):
    await state.update_data(resume_education=message.text.strip())
    await state.set_state(ResumeStates.collecting_experience)
    await message.answer("Опиши ОПЫТ работы (компании, должности, годы, 1-2 ключевые обязанности на каждое место):")

@router.message(ResumeStates.collecting_experience)
async def resume_experience(message: Message, state: FSMContext):
    await state.update_data(resume_experience=message.text.strip())
    await state.set_state(ResumeStates.collecting_skills)
    await message.answer("Перечисли НАВЫКИ (стек, инструменты, методологии):")

@router.message(ResumeStates.collecting_skills)
async def resume_skills(message: Message, state: FSMContext):
    await state.update_data(resume_skills=message.text.strip())
    data = await state.get_data()
    education = data.get("resume_education", "")
    experience = data.get("resume_experience", "")
    skills = data.get("resume_skills", "")

    text = await generate_resume(education, experience, skills)
    await state.clear()
    await message.answer(text, reply_markup=close_mode())
    await message.answer("Готово. Можешь вернуться в меню кнопкой «Закончить».")