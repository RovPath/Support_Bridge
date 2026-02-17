import asyncio
import logging
from typing import Dict, Tuple
from aiogram import Bot, Dispatcher, types

logger = logging.getLogger(__name__)


class BotManager:
    def __init__(self, main_bot: Bot):
        self.main_bot = main_bot
        self.active_bots: Dict[str, dict] = {}  # token → {bot, dp, task, owner_id, username}
        self.notification_targets: Dict[int, int] = {}  # owner_id → target_chat_id
        # (target_chat_id, forwarded_msg_id) → (user_id, support_bot_token)
        self.forwarded_message_map: Dict[Tuple[int, int], Tuple[int, str]] = {}

    def set_notification_target(self, owner_id: int, chat_id: int):
        self.notification_targets[owner_id] = chat_id

    def get_notification_target(self, owner_id: int) -> int:
        return self.notification_targets.get(owner_id, owner_id)

    def register_bot(self, token: str, owner_id: int, bot_username: str):
        if token in self.active_bots:
            raise ValueError("Этот токен уже используется")

        support_bot = Bot(token=token)
        dp = Dispatcher()

        @dp.message()
        async def handle_message(message: types.Message):
            if message.text and message.text.startswith("/"):
                command = message.text.split()[0].lower().strip()
                if command == "/start":
                    await message.answer(
                        "👋 Здравствуйте! Пожалуйста, опишите вашу проблему или задайте вопрос.\n\n"
                        "Ваше сообщение будет передано в поддержку.",
                        parse_mode="HTML",
                    )
                return

            target_chat_id = self.get_notification_target(owner_id)

            user_info = (
                f"📩 Новое обращение из @{bot_username}\n\n"
                f"👤 Пользователь: {message.from_user.full_name} "
                f"(@{message.from_user.username or 'N/A'})\n"
                f"🆔 ID: <code>{message.from_user.id}</code>"
            )

            forwarded_msg = None
            try:
                if message.photo:
                    caption = f"{user_info}\n\n🖼️ Фото"
                    if message.caption:
                        caption += f"\n\n💬 Текст к фото:\n{message.caption}"
                    if len(caption) > 1024:
                        caption = caption[:1021] + "..."
                    forwarded_msg = await self.main_bot.send_photo(
                        chat_id=target_chat_id, photo=message.photo[-1].file_id, caption=caption, parse_mode="HTML"
                    )
                elif message.document:
                    caption = f"{user_info}\n\n📎 Документ: {message.document.file_name}"
                    if message.caption:
                        caption += f"\n\n💬 Описание:\n{message.caption}"
                    if len(caption) > 1024:
                        caption = caption[:1021] + "..."
                    forwarded_msg = await self.main_bot.send_document(
                        chat_id=target_chat_id, document=message.document.file_id, caption=caption, parse_mode="HTML"
                    )
                elif message.text:
                    full_text = f"{user_info}\n\n💬 Сообщение:\n{message.text}"
                    forwarded_msg = await self.main_bot.send_message(
                        chat_id=target_chat_id, text=full_text[:4096], parse_mode="HTML"
                    )
                else:
                    forwarded_msg = await self.main_bot.send_message(
                        chat_id=target_chat_id,
                        text=f"{user_info}\n\n⚠️ Неподдерживаемый тип: {message.content_type}",
                        parse_mode="HTML",
                    )

                if forwarded_msg:
                    # Сохраняем связь: (чат поддержки, ID пересланного сообщения) → (пользователь, токен бота)
                    self.forwarded_message_map[(target_chat_id, forwarded_msg.message_id)] = (
                        message.from_user.id,
                        token,
                    )

                await message.answer("✅ Сообщение отправлено в поддержку!", parse_mode="HTML")

            except Exception as e:
                logger.error(f"Ошибка пересылки для @{bot_username}: {e}", exc_info=True)
                await message.answer("❌ Не удалось отправить сообщение. Попробуйте позже.", parse_mode="HTML")

        task = asyncio.create_task(dp.start_polling(support_bot))

        self.active_bots[token] = {
            "bot": support_bot,
            "dp": dp,
            "task": task,
            "owner_id": owner_id,
            "username": bot_username,
        }

    async def shutdown_all(self):
        tokens = list(self.active_bots.keys())
        for token in tokens:
            data = self.active_bots[token]

            data["task"].cancel()
            try:
                await data["task"]
            except asyncio.CancelledError:
                pass

            try:
                await data["dp"].stop_polling()
            except Exception as e:
                logger.error(f"Ошибка остановки polling для {token}: {e}")

            try:
                await data["bot"].session.close()
            except Exception as e:
                logger.error(f"Ошибка закрытия сессии для {token}: {e}")

            logger.info(f"Бот @{data['username']} остановлен")
            del self.active_bots[token]

        # Опционально: очистить маппинг
        self.forwarded_message_map.clear()
