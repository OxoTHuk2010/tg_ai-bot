import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router
import logging

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.include_routers(router)
    await dp.start_polling(bot)

asyncio.run(main())