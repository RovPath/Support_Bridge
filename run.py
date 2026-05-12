import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from config import BOT_TOKEN, USE_PROXY, PROXY_URL, get_client_session
from database.manager import DBManager
from app.middlewares.l10n import L10nMiddleware
from app.middlewares.bot_manager import BotManager
from app.handlers import start, binding, support_bot, admin_reply, common

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if USE_PROXY and PROXY_URL:
    session = AiohttpSession(proxy=PROXY_URL)
    main_bot = Bot(token=BOT_TOKEN, session=session)
else:
    main_bot = Bot(token=BOT_TOKEN)

db = DBManager()

async def on_startup(dispatcher: Dispatcher):
    logging.info("Starting up...")
    await db.connect()
    bot_manager = BotManager(main_bot, db)
    dispatcher.workflow_data.update(bot_manager=bot_manager)
    dispatcher.update.middleware(L10nMiddleware(db))

async def on_shutdown(dispatcher: Dispatcher):
    logging.info("Shutting down...")
    bot_manager = dispatcher.workflow_data.get("bot_manager")
    if bot_manager:
        await bot_manager.shutdown_all()
    await db.close()
    await main_bot.session.close()

async def main():
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_router(start.router)
    dp.include_router(binding.router)
    dp.include_router(support_bot.router)
    dp.include_router(admin_reply.router)
    dp.include_router(common.router)

    await dp.start_polling(main_bot)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass