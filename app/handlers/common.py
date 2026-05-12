from aiogram import Router, F, types
from app.utils.texts import TEXTS
from app.handlers.start import get_main_keyboard

router = Router()

@router.callback_query(F.data == "status")
async def show_status(callback: types.CallbackQuery, bot_manager, lang: str):
    t = TEXTS.get(lang, TEXTS["ru"])
    user_id = callback.from_user.id

    user_bots = [inst for inst in bot_manager.active_instances.values() if inst.owner_id == user_id]

    if not user_bots:
        text = t["status_no_bots"]
    else:
        target_chat_id = await bot_manager.get_notification_target(user_id)
        if target_chat_id == user_id:
            target_info = t["status_target_ls"]
        else:
            target_info = t["status_target_chat"].format(chat_id=target_chat_id)

        text = (
            t["status_header"] +
            t["status_bots_count"].format(count=len(user_bots)) +
            target_info + "\n\n" +
            t["status_bots_list"]
        )
        for inst in user_bots:
            token_preview = f"{inst.token[:6]}...{inst.token[-4:]}"
            text += t["status_bot_line"].format(username=inst.username, token=token_preview)

    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=get_main_keyboard(lang))
    await callback.answer()

@router.callback_query(F.data == "back")
async def back_callback(callback: types.CallbackQuery, lang: str):
    t = TEXTS.get(lang, TEXTS["ru"])
    await callback.message.edit_text(
        text=t["start"] + "\n\n👇 <b>Выберите действие:</b>",
        parse_mode="HTML",
        reply_markup=get_main_keyboard(lang)
    )
    await callback.answer()