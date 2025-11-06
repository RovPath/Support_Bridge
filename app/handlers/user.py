import logging
from aiogram import Router, F, Bot, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError
from app.states.support_bot import SupportBotRegistration
from app.keyboards.inline import start_kb
from aiogram.exceptions import TelegramBadRequest


logger = logging.getLogger(__name__)

router = Router()


# ───── /start ─────
@router.message(CommandStart())
async def start_menu(message: types.Message):
    text = "Привет! Я <b>SupportBridge</b> — бот для пересылки обращений в поддержку.\n\nВыберите действие:"
    await message.answer(text=text, parse_mode="HTML", reply_markup=start_kb)


# ───── 📬 Получать сюда ─────
@router.callback_query(F.data == "notify_here")
async def notify_here(callback: types.CallbackQuery, bot: Bot, bot_manager):
    owner_id = callback.from_user.id
    chat_id = callback.message.chat.id

    try:
        member = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
        if member.status in ("member", "administrator", "creator"):
            bot_manager.set_notification_target(owner_id, chat_id)
            if chat_id == owner_id:
                text = "✅ Теперь все обращения будут приходить вам в личные сообщения."
            else:
                text = f"✅ Этот чат (ID: <code>{chat_id}</code>) привязан как точка получения обращений!"
            await callback.message.edit_text(text, parse_mode="HTML")
        else:
            await callback.message.edit_text(
                "❌ Бот не добавлен в этот чат. Сначала добавьте бота, затем нажмите кнопку снова.",
                parse_mode="HTML",
            )
    except TelegramAPIError as e:
        await callback.message.edit_text(f"❌ Не удалось проверить чат: {str(e)}", parse_mode="HTML")
        logger.error(f"Ошибка при проверке чата {chat_id}: {e}")

    await callback.answer()


# ───── 🔗 Привязать чат (из ЛС) ─────
@router.callback_query(F.data == "bind_chat")
async def bind_chat(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    if chat_id == user_id:
        await callback.message.edit_text(
            "Вы в личных сообщениях.\n\nПожалуйста, отправьте <b>ID чата или канала</b>, куда должны приходить обращения.\n\n"
            "ℹ️ ID канала/группы — это целое число (например: <code>-1001234567890</code>).",
            parse_mode="HTML",
        )
        await state.set_state(ChatBinding.waiting_for_chat_id)
    else:
        await callback.message.edit_text(
            "Эта кнопка предназначена для привязки <b>другого</b> чата из личных сообщений.\n\n"
            "Чтобы привязать <b>этот</b> чат, используйте кнопку «📬 Получать сюда».",
            parse_mode="HTML",
        )
    await callback.answer()


# ───── FSM: Ввод ID чата ─────
from aiogram.fsm.state import State, StatesGroup


class ChatBinding(StatesGroup):
    waiting_for_chat_id = State()


@router.message(ChatBinding.waiting_for_chat_id)
async def process_chat_id(message: types.Message, state: FSMContext, bot: Bot, bot_manager):
    user_id = message.from_user.id
    try:
        chat_id = int(message.text.strip())
    except ValueError:
        await message.answer(
            "❌ Неверный формат ID. Отправьте целое число (например: <code>-1001234567890</code>).", parse_mode="HTML"
        )
        return

    try:
        member = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
        if member.status in ("member", "administrator", "creator"):
            bot_manager.set_notification_target(user_id, chat_id)
            await message.answer(f"✅ Чат (ID: <code>{chat_id}</code>) успешно привязан!", parse_mode="HTML")
        else:
            await message.answer(
                "❌ Бот не добавлен в указанный чат. Пожалуйста, добавьте бота в чат и повторите попытку.",
                parse_mode="HTML",
            )
    except TelegramAPIError as e:
        if "chat not found" in str(e).lower() or "not found" in str(e).lower():
            await message.answer(
                "❌ Чат с таким ID не найден. Убедитесь, что ID верный и начинается с `-100` для супергрупп/каналов.",
                parse_mode="HTML",
            )
        elif "bot is not a member" in str(e).lower():
            await message.answer(
                "❌ Бот не является участником этого чата. Добавьте его и повторите.", parse_mode="HTML"
            )
        else:
            await message.answer(f"❌ Ошибка при проверке чата: {str(e)}", parse_mode="HTML")
        logger.error(f"Ошибка проверки чата {chat_id}: {e}")

    await state.clear()


# ───── ➕ Создать бота ─────
@router.callback_query(F.data == "create_support_bot")
async def create_support(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Пожалуйста, пришлите токен вашего Telegram-бота.\n\n"
        "❗ Токен можно получить у @BotFather, отправив команду\n/newbot.\n"
        "Он выглядит примерно так:\n<code>8763200231:g261RIR60IAbGgQTxuJ8S2xEIFFXdG044s</code>",
        parse_mode="HTML",
    )
    await state.set_state(SupportBotRegistration.waiting_for_token)
    await callback.answer()


# ───── 📊 Статус ─────


@router.callback_query(F.data == "status")
async def show_status(callback: types.CallbackQuery, bot_manager):
    user_id = callback.from_user.id
    user_bots = [data for data in bot_manager.active_bots.values() if data["owner_id"] == user_id]

    if not user_bots:
        status_text = "ℹ️ У вас пока нет активных ботов.\n\n⚠️ Чтобы начать, нажмите «➕ Создать бота»."
    else:
        target_chat_id = bot_manager.get_notification_target(user_id)
        if target_chat_id == user_id:
            target_info = "в ваши личные сообщения"
        else:
            target_info = f"в чат с ID: <code>{target_chat_id}</code>"

        status_text = (
            f"ℹ️ У вас активно <b>{len(user_bots)}</b> бот(-ов).\n\n📍 Все обращения пересылаются {target_info}.\n\n"
        )
        status_text += "<b>Привязанные боты:</b>\n"
        for data in user_bots:
            username = data["username"]
            token = data["bot"].token
            token_preview = f"{token[:6]}...{token[-4:]}"
            status_text += f"• @{username} (<code>{token_preview}</code>)\n"

    try:
        await callback.message.edit_text(status_text, parse_mode="HTML", reply_markup=start_kb)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e).lower():
            # Игнорируем, если текст не изменился
            pass
        else:
            raise  # Пробрасываем другие ошибки

    await callback.answer()


# ───── 🔄 Обработка токена ─────
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
            location = "вам в личные сообщения"
        else:
            location = f"в чат (ID: <code>{target}</code>)"

        await message.answer(
            f"✅ Бот @{bot_username} успешно привязан!\n"
            f"Теперь все сообщения пользователей будут пересылаться {location}.",
            parse_mode="HTML",
        )
        logger.info(f"Бот @{bot_username} привязан. Владелец: {owner_id}")

    except ValueError as e:
        await message.answer("❌ Этот токен уже используется в системе!", parse_mode="HTML")
    except TelegramAPIError as e:
        error_msg = "Неверный токен бота" if "401" in str(e) else str(e)
        await message.answer(f"❌ Ошибка подключения: {error_msg}", parse_mode="HTML")
        logger.error(f"Ошибка токена {token}: {e}")
    except Exception as e:
        await message.answer(f"❌ Неожиданная ошибка: {str(e)}", parse_mode="HTML")
        logger.exception("Критическая ошибка при регистрации бота")
    finally:
        await state.clear()
