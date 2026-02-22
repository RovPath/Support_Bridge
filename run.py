import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.handlers.user import router as user_router
from app.middlewares.bot_manager import BotManager

load_dotenv()
TG_TOKEN = os.getenv("TG_TOKEN")
if not TG_TOKEN:
    raise ValueError("TG_TOKEN не задан в .env")

main_bot = Bot(token=TG_TOKEN)


async def on_startup(dispatcher: Dispatcher):
    print("Starting up...")
    bot_manager = BotManager(main_bot)
    dispatcher.workflow_data.update(bot_manager=bot_manager)


async def on_shutdown(dispatcher: Dispatcher):
    print("Shutting down...")
    bot_manager = dispatcher.workflow_data.get("bot_manager")
    if bot_manager:
        await bot_manager.shutdown_all()


async def main():
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_router(user_router)
    await dp.start_polling(main_bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
