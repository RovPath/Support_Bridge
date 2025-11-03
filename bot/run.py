import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TG_BOT
from dotenv import load_dotenv


async def main():
    load_dotenv()
    bot = Bot(token=TG_BOT)
    dp = Dispatcher()
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    await dp.start_polling(bot)


async def startup(dispatcher: Dispatcher):
    print("Starting up...")


async def shutdown(dispatcher: Dispatcher):
    print("Shutting down...")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
