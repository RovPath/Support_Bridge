import logging
from html import escape
from aiogram import Router, types
from app.utils.texts import TEXTS
from app.middlewares.bot_manager import BotManager

logger = logging.getLogger(__name__)
router = Router()

@router.message()
async def handle_admin_reply(message: types.Message, bot_manager: BotManager, lang: str):
    t = TEXTS.get(lang, TEXTS["ru"])

    if not message.reply_to_message or not hasattr(message.reply_to_message, "message_id"):
        return

    chat_id = message.chat.id
    replied_msg_id = message.reply_to_message.message_id
    mapping_key = (chat_id, replied_msg_id)

    mapping = bot_manager.forwarded_message_map.get(mapping_key)
    if not mapping:
        return

    user_id, support_bot_token = mapping
    instance = bot_manager.active_instances.get(support_bot_token)
    if not instance:
        await message.reply(t["reply_error_bot_inactive"], parse_mode="HTML")
        return

    support_bot = instance.bot
    content_type = message.content_type

    try:
        if content_type == "text":
            text = escape(message.text)
            await support_bot.send_message(
                user_id,
                t["admin_reply_text"].format(text=text),
                parse_mode="HTML"
            )
            await message.reply(t["reply_success_text"], parse_mode="HTML")

        elif content_type == "sticker":
            await support_bot.send_sticker(user_id, message.sticker.file_id)
            await message.reply(t["reply_success_sticker"], parse_mode="HTML")

        elif content_type == "photo":
            photo = message.photo[-1]
            caption = escape(message.caption) if message.caption else None
            if caption:
                await support_bot.send_photo(
                    user_id, photo.file_id,
                    caption=t["admin_reply_photo_caption"].format(caption=caption),
                    parse_mode="HTML"
                )
            else:
                await support_bot.send_photo(
                    user_id, photo.file_id,
                    caption=t["admin_reply_photo"],
                    parse_mode="HTML"
                )
            await message.reply(t["reply_success_photo"], parse_mode="HTML")

        elif content_type == "video":
            video = message.video
            caption = escape(message.caption) if message.caption else None
            if caption:
                await support_bot.send_video(
                    user_id, video.file_id,
                    caption=t["admin_reply_video_caption"].format(caption=caption),
                    parse_mode="HTML"
                )
            else:
                await support_bot.send_video(
                    user_id, video.file_id,
                    caption=t["admin_reply_video"],
                    parse_mode="HTML"
                )
            await message.reply(t["reply_success_video"], parse_mode="HTML")

        elif content_type == "document":
            doc = message.document
            caption = escape(message.caption) if message.caption else None
            if caption:
                await support_bot.send_document(
                    user_id, doc.file_id,
                    caption=t["admin_reply_document_caption"].format(caption=caption),
                    parse_mode="HTML"
                )
            else:
                await support_bot.send_document(
                    user_id, doc.file_id,
                    caption=t["admin_reply_document"],
                    parse_mode="HTML"
                )
            await message.reply(t["reply_success_document"], parse_mode="HTML")

        elif content_type == "audio":
            audio = message.audio
            caption = escape(message.caption) if message.caption else None
            if caption:
                await support_bot.send_audio(
                    user_id, audio.file_id,
                    caption=t["admin_reply_audio_caption"].format(caption=caption),
                    parse_mode="HTML"
                )
            else:
                await support_bot.send_audio(
                    user_id, audio.file_id,
                    caption=t["admin_reply_audio"],
                    parse_mode="HTML"
                )
            await message.reply(t["reply_success_audio"], parse_mode="HTML")

        elif content_type == "voice":
            voice = message.voice
            caption = escape(message.caption) if message.caption else None
            if caption:
                await support_bot.send_voice(
                    user_id, voice.file_id,
                    caption=t["admin_reply_voice_caption"].format(caption=caption),
                    parse_mode="HTML"
                )
            else:
                await support_bot.send_voice(
                    user_id, voice.file_id,
                    caption=t["admin_reply_voice"],
                    parse_mode="HTML"
                )
            await message.reply(t["reply_success_voice"], parse_mode="HTML")

        elif content_type == "video_note":
            await support_bot.send_video_note(user_id, message.video_note.file_id)
            await message.reply(t["reply_success_video_note"], parse_mode="HTML")

        elif content_type == "animation":
            anim = message.animation
            caption = escape(message.caption) if message.caption else None
            if caption:
                await support_bot.send_animation(
                    user_id, anim.file_id,
                    caption=t["admin_reply_animation_caption"].format(caption=caption),
                    parse_mode="HTML"
                )
            else:
                await support_bot.send_animation(
                    user_id, anim.file_id,
                    caption=t["admin_reply_animation"],
                    parse_mode="HTML"
                )
            await message.reply(t["reply_success_animation"], parse_mode="HTML")

        else:
            await message.reply(
                t["reply_error_unsupported"].format(type=content_type),
                parse_mode="HTML"
            )
    except Exception as e:
        logger.exception(f"Ошибка отправки ответа {content_type}")
        error_str = str(e).lower()
        if "file is too big" in error_str:
            await message.reply(t["reply_error_file_too_big"], parse_mode="HTML")
        elif "wrong file identifier" in error_str:
            await message.reply(t["reply_error_wrong_file_id"], parse_mode="HTML")
        elif "chat not found" in error_str:
            await message.reply(t["reply_error_chat_not_found"], parse_mode="HTML")
        else:
            await message.reply(
                t["reply_error_unknown"].format(error=str(e)[:100]),
                parse_mode="HTML"
            )