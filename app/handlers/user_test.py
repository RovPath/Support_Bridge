import logging
from aiogram import Router, F, Bot, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError
from app.states.support_bot import SupportBotRegistration, ChatBinding
from app.keyboards.inline import start_kb, back_kb
from aiogram.exceptions import TelegramBadRequest
from html import escape

logger = logging.getLogger(__name__)

router = Router()


# ───── /start ─────
@router.message(CommandStart())
async def start_menu(message: types.Message):
    """Главное меню бота"""
    text = (
        "👋 <b>Добро пожаловать в SupportBridge!</b>\n\n"
        "Я помогаю создавать ботов для поддержки и перенаправлять "
        "обращения пользователей в удобное для вас место.\n\n"
        "📌 <b>Что я умею:</b>\n"
        "• Создавать ботов поддержки\n"
        "• Привязывать чаты для получения обращений\n"
        "• Пересылать сообщения от пользователей\n\n"
        "👇 <b>Выберите действие:</b>"
    )
    await message.answer(text=text, parse_mode="HTML", reply_markup=start_kb)


# ───── 📬 Получать сюда ─────
@router.callback_query(F.data == "notify_here")
async def notify_here(callback: types.CallbackQuery, bot: Bot, bot_manager):
    """Привязка текущего чата для получения уведомлений"""
    owner_id = callback.from_user.id
    chat_id = callback.message.chat.id

    try:
        # Проверяем, есть ли бот в чате
        member = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)

        if member.status in ("member", "administrator", "creator"):
            bot_manager.set_notification_target(owner_id, chat_id)

            if chat_id == owner_id:
                text = "✅ <b>Готово!</b>\nТеперь все обращения будут приходить вам в личные сообщения."
            else:
                text = (
                    f"✅ <b>Чат успешно привязан!</b>\n\n"
                    f"📢 Все обращения будут приходить в этот чат.\n"
                    f"🆔 ID чата: <code>{chat_id}</code>"
                )

            await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_kb)
        else:
            await callback.message.edit_text(
                "❌ <b>Бот не добавлен в этот чат</b>\n\n" "Сначала добавьте бота в чат, затем нажмите кнопку снова.",
                parse_mode="HTML",
                reply_markup=back_kb,
            )
    except TelegramAPIError as e:
        error_text = f"❌ <b>Ошибка при проверке чата</b>\n\n{str(e)}"
        await callback.message.edit_text(error_text, parse_mode="HTML")
        logger.error(f"Ошибка при проверке чата {chat_id}: {e}")

    await callback.answer()


# ───── 🔗 Привязать чат (из ЛС) ─────
@router.callback_query(F.data == "bind_chat")
async def bind_chat(callback: types.CallbackQuery, state: FSMContext):
    """Начало привязки другого чата (из ЛС)"""
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    if chat_id == user_id:
        text = (
            "🔗 <b>Привязка другого чата</b>\n\n"
            "Пожалуйста, отправьте <b>ID чата или канала</b>, "
            "куда должны приходить обращения.\n\n"
            "ℹ️ <b>Как получить ID:</b>\n"
            "• Для канала/группы: добавьте бота @IDCollectors_bot\n"
            "• ID должен быть числом (например: <code>-1001234567890</code>)\n\n"
            "📝 <b>Отправьте ID:</b>"
        )
        await callback.message.edit_text(text, parse_mode="HTML")
        await state.set_state(ChatBinding.waiting_for_chat_id)
    else:
        text = (
            "❌ <b>Неверное действие</b>\n\n"
            "Эта кнопка предназначена для привязки <b>другого</b> чата "
            "из личных сообщений.\n\n"
            "Чтобы привязать <b>этот</b> чат, используйте кнопку "
            "«📬 Получать сюда»."
        )
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_kb)

    await callback.answer()


# ───── FSM: Обработка ID чата ─────
@router.message(ChatBinding.waiting_for_chat_id)
async def process_chat_id(message: types.Message, state: FSMContext, bot: Bot, bot_manager):
    """Обработка введенного ID чата"""
    user_id = message.from_user.id

    # Парсим ID
    try:
        chat_id = int(message.text.strip())
    except ValueError:
        await message.answer(
            "❌ <b>Неверный формат</b>\n\n" "ID должен быть целым числом.\n" "Пример: <code>-1001234567890</code>",
            parse_mode="HTML",
        )
        return

    # Проверяем чат
    try:
        member = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)

        if member.status in ("member", "administrator", "creator"):
            bot_manager.set_notification_target(user_id, chat_id)

            success_text = (
                f"✅ <b>Чат успешно привязан!</b>\n\n"
                f"🆔 ID: <code>{chat_id}</code>\n"
                f"📬 Все обращения будут приходить сюда."
            )
            await message.answer(success_text, parse_mode="HTML")
        else:
            await message.answer(
                "❌ <b>Бот не в чате</b>\n\n" "Сначала добавьте бота в указанный чат, затем повторите попытку.",
                parse_mode="HTML",
            )

    except TelegramAPIError as e:
        error_msg = str(e).lower()

        if "chat not found" in error_msg or "not found" in error_msg:
            text = (
                "❌ <b>Чат не найден</b>\n\n"
                "Проверьте правильность ID:\n"
                "• Для групп ID начинается с -100\n"
                "• Убедитесь, что бот добавлен в чат"
            )
        elif "bot is not a member" in error_msg:
            text = "❌ <b>Бот не является участником этого чата</b>\n\nДобавьте его и повторите."
        else:
            text = f"❌ <b>Ошибка при проверке чата</b>\n\n{str(e)}"

        await message.answer(text, parse_mode="HTML")
        logger.error(f"Ошибка проверки чата {chat_id}: {e}")

    await state.clear()


# ───── ➕ Создать бота ─────
@router.callback_query(F.data == "create_support_bot")
async def create_support(callback: types.CallbackQuery, state: FSMContext):
    """Начало создания бота поддержки"""
    text = (
        "🤖 <b>Создание бота поддержки</b>\n\n"
        "Пожалуйста, пришлите токен вашего Telegram-бота.\n\n"
        "🔑 <b>Как получить токен:</b>\n"
        "1. Найдите @BotFather в Telegram\n"
        "2. Отправьте команду /newbot\n"
        "3. Следуйте инструкциям\n"
        "4. Скопируйте полученный токен\n\n"
        "📝 <b>Пример токена:</b>\n"
        "<code>8763200231:g261RIR60IAbGgQTxuJ8S2xEIFFXdG044s</code>\n\n"
        "👇 <b>Отправьте токен:</b>"
    )

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=back_kb,
    )
    await state.set_state(SupportBotRegistration.waiting_for_token)
    await callback.answer()


# ───── 📊 Статус ─────
@router.callback_query(F.data == "status")
async def show_status(callback: types.CallbackQuery, bot_manager):
    """Показ статуса ботов пользователя"""
    user_id = callback.from_user.id
    user_bots = [data for data in bot_manager.active_bots.values() if data["owner_id"] == user_id]

    if not user_bots:
        status_text = (
            "ℹ️ <b>У вас пока нет активных ботов</b>\n\n" "Чтобы начать, нажмите «➕ Создать бота» в главном меню."
        )
    else:
        target_chat_id = bot_manager.get_notification_target(user_id)

        if target_chat_id == user_id:
            target_info = "📬 в ваши личные сообщения"
        else:
            target_info = f"📬 в чат с ID: <code>{target_chat_id}</code>"

        status_text = (
            f"📊 <b>Статистика</b>\n\n"
            f"🤖 Активных ботов: <b>{len(user_bots)}</b>\n"
            f"{target_info}\n\n"
            f"<b>📋 Список ботов:</b>\n"
        )

        for data in user_bots:
            username = data["username"]
            token = data["bot"].token
            token_preview = f"{token[:6]}...{token[-4:]}"
            status_text += f"• @{username} (<code>{token_preview}</code>)\n"

    try:
        await callback.message.edit_text(status_text, parse_mode="HTML", reply_markup=start_kb)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e).lower():
            raise

    await callback.answer()


# ───── 🔄 Обработка токена ─────
@router.message(SupportBotRegistration.waiting_for_token)
async def process_bot_token(message: types.Message, state: FSMContext, bot: Bot, bot_manager):
    """Обработка полученного токена бота"""
    token = message.text.strip()
    owner_id = message.from_user.id

    try:
        # Проверяем токен
        support_bot = Bot(token=token)
        bot_info = await support_bot.get_me()
        bot_username = bot_info.username

        # Регистрируем бота
        bot_manager.register_bot(token, owner_id, bot_username)

        # Определяем куда будут приходить сообщения
        target = bot_manager.get_notification_target(owner_id)
        if target == owner_id:
            location = "📬 вам в личные сообщения"
        else:
            location = f"📬 в чат (ID: <code>{target}</code>)"

        success_text = (
            f"✅ <b>Бот успешно создан!</b>\n\n"
            f"🤖 Имя: @{bot_username}\n"
            f"{location}\n\n"
            f"Теперь все сообщения пользователей будут автоматически "
            f"пересылаться в указанное место."
        )

        await message.answer(success_text, parse_mode="HTML")
        logger.info(f"Бот @{bot_username} привязан. Владелец: {owner_id}")

    except ValueError as e:
        await message.answer(
            "❌ <b>Токен уже используется</b>\n\n" "Этот токен уже зарегистрирован в системе.", parse_mode="HTML"
        )
    except TelegramAPIError as e:
        if "401" in str(e):
            error_msg = "❌ Неверный токен бота. Проверьте правильность токена."
        else:
            error_msg = f"❌ Ошибка подключения: {str(e)}"

        await message.answer(error_msg, parse_mode="HTML")
        logger.error(f"Ошибка токена {token}: {e}")
    except Exception as e:
        await message.answer(f"❌ <b>Неожиданная ошибка</b>\n\n{str(e)}", parse_mode="HTML")
        logger.exception("Критическая ошибка при регистрации бота")
    finally:
        await state.clear()


# ───── ↩️ Назад ─────
@router.callback_query(F.data == "back")
async def back_callback(callback: types.CallbackQuery):
    """Возврат в главное меню"""
    text = (
        "👋 <b>Добро пожаловать в SupportBridge!</b>\n\n"
        "Я помогаю создавать ботов для поддержки и перенаправлять "
        "обращения пользователей в удобное для вас место.\n\n"
        "👇 <b>Выберите действие:</b>"
    )
    await callback.message.edit_text(text=text, parse_mode="HTML", reply_markup=start_kb)
    await callback.answer()


# ───── Обработка ответов администратора ─────
@router.message()
async def handle_admin_reply(message: types.Message, bot_manager):
    """Обработка ответов администратора на сообщения пользователей"""
    if not message.reply_to_message:
        return

    if not hasattr(message.reply_to_message, "message_id"):
        logger.debug("reply_to_message не содержит message_id")
        return

    chat_id = message.chat.id
    replied_msg_id = message.reply_to_message.message_id
    key = (chat_id, replied_msg_id)

    logger.debug(f"🔍 Ищу ключ: {key}")

    mapping = bot_manager.forwarded_message_map.get(key)
    if not mapping:
        logger.debug(f"🚫 Ключ не найден")
        return

    user_id, support_bot_token = mapping

    if support_bot_token not in bot_manager.active_bots:
        try:
            await message.reply(
                "❌ <b>Бот отключён</b>\n\n" "Бот, через который пришло обращение, больше не активен.",
                parse_mode="HTML",
            )
        except:
            pass
        return

    support_bot = bot_manager.active_bots[support_bot_token]["bot"]
    content_type = message.content_type

    logger.info(f"📨 Обработка {content_type} в ответе")

    try:
        # Текстовые сообщения
        if content_type == "text":
            text = escape(message.text)
            msg = f"📨 <b>Ответ от поддержки:</b>\n\n{text}"
            await support_bot.send_message(user_id, msg, parse_mode="HTML")
            await message.reply("✅ Текстовый ответ отправлен пользователю.", parse_mode="HTML")

        # Стикеры
        elif content_type == "sticker":
            await support_bot.send_sticker(user_id, message.sticker.file_id)
            await message.reply("✅ Стикер отправлен пользователю.", parse_mode="HTML")

        # Фото
        elif content_type == "photo":
            photo = message.photo[-1]  # Берем самое качественное фото
            caption = escape(message.caption) if message.caption else None

            if caption:
                await support_bot.send_photo(
                    user_id,
                    photo.file_id,
                    caption=f"📸 <b>Ответ от поддержки (фото):</b>\n\n{caption}",
                    parse_mode="HTML",
                )
            else:
                await support_bot.send_photo(
                    user_id, photo.file_id, caption="📸 <b>Ответ от поддержки (фото)</b>", parse_mode="HTML"
                )
            await message.reply("✅ Фото отправлено пользователю.", parse_mode="HTML")

        # Видео
        elif content_type == "video":
            video = message.video
            caption = escape(message.caption) if message.caption else None

            if caption:
                await support_bot.send_video(
                    user_id,
                    video.file_id,
                    caption=f"🎥 <b>Ответ от поддержки (видео):</b>\n\n{caption}",
                    parse_mode="HTML",
                )
            else:
                await support_bot.send_video(
                    user_id, video.file_id, caption="🎥 <b>Ответ от поддержки (видео)</b>", parse_mode="HTML"
                )
            await message.reply("✅ Видео отправлено пользователю.", parse_mode="HTML")

        # Документы
        elif content_type == "document":
            document = message.document
            caption = escape(message.caption) if message.caption else None

            if caption:
                await support_bot.send_document(
                    user_id,
                    document.file_id,
                    caption=f"📎 <b>Ответ от поддержки (документ):</b>\n\n{caption}",
                    parse_mode="HTML",
                )
            else:
                await support_bot.send_document(
                    user_id, document.file_id, caption="📎 <b>Ответ от поддержки (документ)</b>", parse_mode="HTML"
                )
            await message.reply("✅ Документ отправлен пользователю.", parse_mode="HTML")

        # Аудио
        elif content_type == "audio":
            audio = message.audio
            caption = escape(message.caption) if message.caption else None

            if caption:
                await support_bot.send_audio(
                    user_id,
                    audio.file_id,
                    caption=f"🎵 <b>Ответ от поддержки (аудио):</b>\n\n{caption}",
                    parse_mode="HTML",
                )
            else:
                await support_bot.send_audio(
                    user_id, audio.file_id, caption="🎵 <b>Ответ от поддержки (аудио)</b>", parse_mode="HTML"
                )
            await message.reply("✅ Аудио отправлено пользователю.", parse_mode="HTML")

        # Голосовые сообщения
        elif content_type == "voice":
            voice = message.voice
            caption = escape(message.caption) if message.caption else None

            if caption:
                await support_bot.send_voice(
                    user_id,
                    voice.file_id,
                    caption=f"🎤 <b>Ответ от поддержки (голосовое):</b>\n\n{caption}",
                    parse_mode="HTML",
                )
            else:
                await support_bot.send_voice(
                    user_id, voice.file_id, caption="🎤 <b>Ответ от поддержки (голосовое)</b>", parse_mode="HTML"
                )
            await message.reply("✅ Голосовое сообщение отправлено пользователю.", parse_mode="HTML")

        # Видеосообщения (кружочки)
        elif content_type == "video_note":
            video_note = message.video_note
            await support_bot.send_video_note(user_id, video_note.file_id)
            await message.reply("✅ Видеосообщение отправлено пользователю.", parse_mode="HTML")

        # Анимации (GIF)
        elif content_type == "animation":
            animation = message.animation
            caption = escape(message.caption) if message.caption else None

            if caption:
                await support_bot.send_animation(
                    user_id,
                    animation.file_id,
                    caption=f"🎬 <b>Ответ от поддержки (GIF):</b>\n\n{caption}",
                    parse_mode="HTML",
                )
            else:
                await support_bot.send_animation(
                    user_id, animation.file_id, caption="🎬 <b>Ответ от поддержки (GIF)</b>", parse_mode="HTML"
                )
            await message.reply("✅ GIF отправлен пользователю.", parse_mode="HTML")

        # Медиагруппы (альбомы)
        elif content_type in ["photo", "video"] and message.media_group_id:
            # Это обрабатывается отдельно через middleware или другой хендлер
            # Пока просто уведомляем пользователя
            await message.reply(
                "⚠️ <b>Альбомы пока не поддерживаются</b>\n\n" "Пожалуйста, отправляйте фото и видео по отдельности.",
                parse_mode="HTML",
            )

        else:
            # Неподдерживаемый тип
            await message.reply(
                "⚠️ <b>Неподдерживаемый тип контента</b>\n\n"
                "В текущей версии можно отвечать:\n"
                "• Текстом\n"
                "• Фото\n"
                "• Видео\n"
                "• Документами\n"
                "• Аудио\n"
                "• Голосовыми\n"
                "• Стикерами\n"
                "• GIF\n\n"
                f"Тип полученного сообщения: {content_type}",
                parse_mode="HTML",
            )
            logger.warning(f"Попытка отправить неподдерживаемый тип: {content_type}")

    except Exception as e:
        logger.exception(f"❌ Ошибка при отправке {content_type} ответа")

        error_message = str(e)
        user_friendly_error = "❌ <b>Ошибка при отправке ответа</b>\n\n"

        if "file is too big" in error_message.lower():
            user_friendly_error += "Файл слишком большой для отправки через Telegram."
        elif "wrong file identifier" in error_message.lower():
            user_friendly_error += "Не удалось обработать файл. Возможно, он устарел."
        elif "chat not found" in error_message.lower():
            user_friendly_error += "Пользователь заблокировал бота или удалил чат."
        else:
            user_friendly_error += f"Техническая ошибка: {error_message[:100]}..."

        try:
            await message.reply(user_friendly_error, parse_mode="HTML")
        except:
            pass
