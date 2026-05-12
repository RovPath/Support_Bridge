from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.utils.texts import TEXTS

router = Router()

def get_main_keyboard(lang: str) -> InlineKeyboardMarkup:
    t = TEXTS.get(lang, TEXTS["ru"])
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t["btn_notify_here"], callback_data="notify_here"),
                InlineKeyboardButton(text=t["btn_bind_chat"], callback_data="bind_chat"),
            ],
            [
                InlineKeyboardButton(text=t["btn_create_bot"], callback_data="create_support_bot"),
                InlineKeyboardButton(text=t["btn_status"], callback_data="status"),
            ],
        ]
    )

@router.message(CommandStart())
async def cmd_start(message: types.Message, lang: str):
    t = TEXTS.get(lang, TEXTS["ru"])
    await message.answer(
        text=t["start"] + "\n\n👇 <b>Выберите действие:</b>",
        parse_mode="HTML",
        reply_markup=get_main_keyboard(lang)
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message, lang: str):
    t = TEXTS.get(lang, TEXTS["ru"])
    await message.answer(t["help"], parse_mode="HTML")