from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from keyboards.inline import reco_category_keyboard, reco_items_keyboard
from services.reco_service import get_recommendations_structured
from states import RecoStates

router = Router()

@router.callback_query(F.data == "recommendations")
async def reco_entry(call: CallbackQuery, state: FSMContext):
    await state.set_state(RecoStates.choosing_category)
    await state.update_data(reco_blacklist=[], reco_items=[])
    await call.message.answer("Выберите категорию:", reply_markup=reco_category_keyboard())
    await call.answer()

@router.callback_query(F.data.startswith("reco_cat:"))
async def reco_set_cat(call: CallbackQuery, state: FSMContext):
    cat = call.data.split(":", 1)[-1]
    await state.update_data(reco_category=cat)
    await state.set_state(RecoStates.waiting_genre)
    await call.message.answer(f"Категория: {cat}. Введите жанр (например, 'детектив', 'sci-fi', 'джаз'):")
    await call.answer()

@router.message(RecoStates.waiting_genre)
async def reco_get(message: Message, state: FSMContext):
    data = await state.get_data()
    cat = data.get("reco_category", "films")
    bl = data.get("reco_blacklist", [])
    genre = message.text.strip()
    items = await get_recommendations_structured(cat, genre, bl)
    if not items:
        await message.answer("Не удалось сформировать рекомендации. Попробуйте другой жанр.")
        return

    await state.update_data(reco_genre=genre, reco_items=items)
    lines = [f"Рекомендации для {cat}/{genre}:"]
    for i, it in enumerate(items, 1):
        lines.append(f"{i}. {it['title']}\n   {it['why']}")
    await message.answer("\n\n".join(lines), reply_markup=reco_items_keyboard(items))

@router.callback_query(F.data.startswith("reco_dislike:"))
async def reco_dislike(call: CallbackQuery, state: FSMContext):
    idx_str = call.data.split(":", 1)[-1]
    try:
        idx = int(idx_str) - 1
    except ValueError:
        await call.answer("Некорректный выбор", show_alert=True)
        return

    data = await state.get_data()
    items = data.get("reco_items", [])
    if idx < 0 or idx >= len(items):
        await call.answer("Пункт не найден", show_alert=True)
        return

    title = items[idx].get("title")
    bl = data.get("reco_blacklist", [])
    if title and title not in bl:
        bl.append(title)

    cat = data.get("reco_category", "films")
    genre = data.get("reco_genre", "")
    new_items = await get_recommendations_structured(cat, genre, bl)

    await state.update_data(reco_blacklist=bl, reco_items=new_items)

    if not new_items:
        await call.message.answer("Больше вариантов нет. Измените жанр или категорию в главном меню.")
        await call.answer()
        return

    lines = [f"Обновлённые рекомендации для {cat}/{genre} (исключены: {', '.join(bl)})"]
    for i, it in enumerate(new_items, 1):
        lines.append(f"{i}. {it['title']}\n   {it['why']}")
    await call.message.answer("\n\n".join(lines), reply_markup=reco_items_keyboard(new_items))
    await call.answer("Учёл ваш выбор «не нравится».")