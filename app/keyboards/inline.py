from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔗 Привязать чат", callback_data="bind_chat"),
            InlineKeyboardButton(text="📬 Получать сюда", callback_data="notify_here"),
        ],
        [InlineKeyboardButton(text="🤖 Создать бота для принятия сообщений", callback_data="create_support_bot")],
        # [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")],
        [InlineKeyboardButton(text="ℹ️ Статус", callback_data="status")],
    ]
)
