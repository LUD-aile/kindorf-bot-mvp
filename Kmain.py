import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from config import BOT_TOKEN
from handlers import common, team, project, partner

logging.basicConfig(level=logging.INFO)

async def main():
    # Настройка прокси строго через сессию aiohttp
    session = AiohttpSession(proxy="http://proxy.server:3128")

    bot = Bot(token=BOT_TOKEN, session=session)
    dp = Dispatcher()

    dp.include_router(common.router)
    dp.include_router(team.router)
    dp.include_router(project.router)
    dp.include_router(partner.router)

    print("--- ЖЕСТКИЙ ПРОКСИ СЕССИИ АКТИВИРОВАН! ЗАПУСК... ---")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
