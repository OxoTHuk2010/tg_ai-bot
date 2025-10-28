from aiogram.fsm.context import FSMContext

async def init_quiz(state: FSMContext):
    await state.update_data(score = 0, topic=None, question=None)

async def increase_score(state: FSMContext):
    data = await state.get_data()
    score = data.get('score', 0) + 1
    await state.update_data(score=score)
    return score

async def get_score(state: FSMContext) -> int:
    data = await state.get_data()
    return data.get('score',0)