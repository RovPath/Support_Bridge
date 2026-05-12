from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError
from app.states.support_bot import SupportBotStates
from app.utils.texts import TEXTS
from app.middlewares.bot_manager import BotManager

router = Router()

@router.callback_query(F.data == "notify_here")
async def notify_here(
    callback: types.CallbackQuery,
    bot: Bot,
    bot_manager: BotManager,
    lang: str
):
    t = TEXTS.get(lang, TEXTS["ru"])
    owner_id = callback.from_user.id
    chat_id = callback.message.chat.id

    try:
        member = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
        if member.status in ("member", "administrator", "creator"):
            await bot_manager.set_notification_target(owner_id, chat_id)

            if chat_id == owner_id:
                text = t["notify_here_success_ls"]
            else:
                text = t["notify_here_success_chat"].format(chat_id=chat_id)

            await callback.message.edit_text(text, parse_mode="HTML")
        else:
            await callback.message.edit_text(
                t["notify_here_error_not_member"],
                parse_mode="HTML"
            )
    except TelegramAPIError as e:
        await callback.message.edit_text(
            f"❌ <b>Ошибка</b>\n\n{str(e)}",
            parse_mode="HTML"
        )
    await callback.answer()

@router.callback_query(F.data == "bind_chat")
async def bind_chat(
    callback: types.CallbackQuery,
    state: FSMContext,
    lang: str
):
    t = TEXTS.get(lang, TEXTS["ru"])
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    if chat_id == user_id:
        await callback.message.edit_text(
            t["bind_chat_prompt"],
            parse_mode="HTML"
        )
        await state.set_state(SupportBotStates.waiting_for_chat_id)
    else:
        await callback.message.edit_text(
            t["bind_chat_error_wrong_place"],
            parse_mode="HTML"
        )
    await callback.answer()

@router.message(SupportBotStates.waiting_for_chat_id)
async def process_chat_id(
    message: types.Message,
    state: FSMContext,
    bot: Bot,
    bot_manager: BotManager,
    lang: str
):
    t = TEXTS.get(lang, TEXTS["ru"])
    user_id = message.from_user.id

    try:
        chat_id = int(message.text.strip())
    except ValueError:
        await message.answer(t["invalid_chat_id_format"], parse_mode="HTML")
        return

    try:
        member = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
        if member.status in ("member", "administrator", "creator"):
            await bot_manager.set_notification_target(user_id, chat_id)
            await message.answer(
                t["chat_bind_success"].format(chat_id=chat_id),
                parse_mode="HTML"
            )
        else:
            await message.answer(t["chat_bind_error_not_member"], parse_mode="HTML")
    except TelegramAPIError as e:
        error_str = str(e).lower()
        if "chat not found" in error_str or "not found" in error_str:
            await message.answer(t["chat_bind_not_found"], parse_mode="HTML")
        else:
            await message.answer(t["chat_bind_error"].format(error=str(e)), parse_mode="HTML")

    await state.clear()