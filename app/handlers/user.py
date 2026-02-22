import logging
from html import escape
from aiogram import Router, F, Bot, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest
from app.states.support_bot import SupportBotRegistration, ChatBinding
from app.keyboards.inline import start_kb, back_kb

logger = logging.getLogger(__name__)
router = Router()

START_TEXT = (
    "👋 <b>Добро пожаловать в SupportBridge!</b>\n\n"
    "Я помогаю создавать ботов для поддержки и перенаправлять "
    "обращения пользователей в удобное для вас место.\n\n"
    "📌 <b>Что я умею:</b>\n"
    "• Создавать ботов поддержки\n"
    "• Привязывать чаты для получения обращений\n"
    "• Пересылать сообщения от пользователей\n\n"
    "👇 <b>Выберите действие:</b>"
)


@router.message(CommandStart())
async def start_menu(message: types.Message):
    await message.answer(text=START_TEXT, parse_mode="HTML", reply_markup=start_kb)


@router.callback_query(F.data == "notify_here")
async def notify_here(callback: types.CallbackQuery, bot: Bot, bot_manager):
    owner_id = callback.from_user.id
    chat_id = callback.message.chat.id

    try:
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
                "❌ <b>Бот не добавлен в этот чат</b>\n\nСначала добавьте бота в чат, затем нажмите кнопку снова.",
                parse_mode="HTML",
                reply_markup=back_kb,
            )
    except TelegramAPIError as e:
        await callback.message.edit_text(f"❌ <b>Ошибка при проверке чата</b>\n\n{str(e)}", parse_mode="HTML")
        logger.error(f"Ошибка при проверке чата {chat_id}: {e}")
    await callback.answer()


@router.callback_query(F.data == "bind_chat")
async def bind_chat(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    if chat_id == user_id:
        text = (
            "🔗 <b>Привязка другого чата</b>\n\n"
            "Пожалуйста, отправьте <b>ID чата или канала</b>, "
            "куда должны приходить обращения.\n\n"
            "ℹ️ <b>Как получить ID:</b>\n"
            "• Для канала/группы: добавьте бота @Getmyid_bot\n"
            "• ID должен быть числом (например: <code>-1001234567890</code>)\n\n"
            "📝 <b>Отправьте ID:</b>"
        )
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_kb)
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


@router.callback_query(F.data == "create_support_bot")
async def create_support(callback: types.CallbackQuery, state: FSMContext):
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
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_kb)
    await state.set_state(SupportBotRegistration.waiting_for_token)
    await callback.answer()


@router.callback_query(F.data == "status")
async def show_status(callback: types.CallbackQuery, bot_manager):
    user_id = callback.from_user.id
    user_bots = [data for data in bot_manager.active_instances.values() if data.owner_id == user_id]

    if not user_bots:
        status_text = (
            "ℹ️ <b>У вас пока нет активных ботов</b>\n\n"
            "Чтобы начать, нажмите «🤖 Создать бота для принятия сообщений» в главном меню."
        )
    else:
        target_chat_id = bot_manager.get_notification_target(user_id)
        if target_chat_id == user_id:
            target_info = "📬 В ваши личные сообщения"
        else:
            target_info = f"📬 В чат с <b>ID:</b> <code>{target_chat_id}</code>"

        status_text = (
            f"📊 <b>Статистика</b>\n\n"
            f"🤖 Активных ботов: <b>{len(user_bots)}</b>\n"
            f"{target_info}\n\n"
            f"<b>📋 Список ботов:</b>\n"
        )
        for instance in user_bots:
            token_preview = f"{instance.token[:6]}...{instance.token[-4:]}"
            status_text += f"• @{instance.username} (<code>{token_preview}</code>)\n"

    try:
        await callback.message.edit_text(status_text, parse_mode="HTML", reply_markup=start_kb)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e).lower():
            raise
    await callback.answer()


@router.callback_query(F.data == "back")
async def back_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(text=START_TEXT, parse_mode="HTML", reply_markup=start_kb)
    await callback.answer()


@router.message(ChatBinding.waiting_for_chat_id)
async def process_chat_id(message: types.Message, state: FSMContext, bot: Bot, bot_manager):
    user_id = message.from_user.id

    try:
        chat_id = int(message.text.strip())
    except ValueError:
        await message.answer(
            "❌ <b>Неверный формат</b>\n\nID должен быть целым числом.\nПример: <code>-1001234567890</code>",
            parse_mode="HTML",
        )
        return

    try:
        member = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
        if member.status in ("member", "administrator", "creator"):
            bot_manager.set_notification_target(user_id, chat_id)
            await message.answer(
                f"✅ <b>Чат успешно привязан!</b>\n\n🆔 <b>ID:</b> <code>{chat_id}</code>\n📬 Все обращения будут приходить сюда.",
                parse_mode="HTML",
            )
        else:
            await message.answer(
                "❌ <b>Бот не в чате</b>\n\nСначала добавьте бота в указанный чат, затем повторите попытку.",
                parse_mode="HTML",
            )
    except TelegramAPIError as e:
        error_msg = str(e).lower()
        if "chat not found" in error_msg or "not found" in error_msg:
            text = "❌ <b>Чат не найден</b>\n\nПроверьте правильность ID и что бот добавлен в чат."
        elif "bot is not a member" in error_msg:
            text = "❌ <b>Бот не является участником этого чата</b>\n\nДобавьте его и повторите."
        else:
            text = f"❌ <b>Ошибка при проверке чата</b>\n\n{str(e)}"
        await message.answer(text, parse_mode="HTML")
        logger.error(f"Ошибка проверки чата {chat_id}: {e}")
    await state.clear()


@router.message(SupportBotRegistration.waiting_for_token)
async def process_bot_token(message: types.Message, state: FSMContext, bot: Bot, bot_manager):
    token = message.text.strip()
    owner_id = message.from_user.id

    try:
        support_bot = Bot(token=token)
        bot_info = await support_bot.get_me()
        bot_username = bot_info.username

        bot_manager.register_bot(token, owner_id, bot_username)

        target = bot_manager.get_notification_target(owner_id)
        if target == owner_id:
            location = "📬 Вам в личные сообщения"
        else:
            location = f"📬 В чат (ID: <code>{target}</code>)"

        await message.answer(
            f"✅ <b>Бот успешно создан!</b>\n\n🤖 Имя: @{bot_username}\n{location}\n\n"
            f"Теперь все сообщения пользователей будут автоматически пересылаться в указанное место.",
            parse_mode="HTML",
            reply_markup=back_kb,
        )
        logger.info(f"Бот @{bot_username} привязан. Владелец: {owner_id}")

    except ValueError as e:
        await message.answer(
            "❌ <b>Токен уже используется</b>\n\nЭтот токен уже зарегистрирован в системе.", parse_mode="HTML"
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


@router.message()
async def handle_admin_reply(message: types.Message, bot_manager):
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
        await message.reply(
            "❌ <b>Бот отключён</b>\n\nБот, через который пришло обращение, больше не активен.", parse_mode="HTML"
        )
        return

    support_bot = instance.bot
    content_type = message.content_type

    try:
        if content_type == "text":
            text = escape(message.text)
            await support_bot.send_message(user_id, f"📨 <b>Ответ от поддержки:</b>\n\n{text}", parse_mode="HTML")
            await message.reply("✅ Текстовый ответ отправлен пользователю.", parse_mode="HTML")

        elif content_type == "sticker":
            await support_bot.send_sticker(user_id, message.sticker.file_id)
            await message.reply("✅ Стикер отправлен пользователю.", parse_mode="HTML")

        elif content_type == "photo":
            photo = message.photo[-1]
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

        else:
            await message.reply(
                "⚠️ <b>Неподдерживаемый тип контента</b>\n\n"
                "В текущей версии можно отвечать:\n"
                "• Текст\n• Фото\n• Стикеры",
                parse_mode="HTML",
            )

    except Exception as e:
        logger.exception(f"❌ Ошибка при отправке ответа")
        error_msg = str(e).lower()
        if "file is too big" in error_msg:
            text = "❌ Файл слишком большой для отправки через Telegram."
        elif "wrong file identifier" in error_msg:
            text = "❌ Не удалось обработать файл. Возможно, он устарел."
        elif "chat not found" in error_msg:
            text = "❌ Пользователь заблокировал бота или удалил чат."
        else:
            text = f"❌ Техническая ошибка: {str(e)[:100]}..."
        try:
            await message.reply(f"❌ <b>Ошибка при отправке ответа</b>\n\n{text}", parse_mode="HTML")
        except:
            pass
