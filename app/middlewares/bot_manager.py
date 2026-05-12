import asyncio
import logging
from typing import Dict, Tuple, Optional
from aiogram import Bot, Dispatcher, types
from aiogram.client.session.aiohttp import AiohttpSession
from config import USE_PROXY, PROXY_URL

logger = logging.getLogger(__name__)

class BotInstance:
    def __init__(self, token: str, owner_id: int, username: str, manager: "BotManager"):
        self.token = token
        self.owner_id = owner_id
        self.username = username
        self.manager = manager
        if USE_PROXY and PROXY_URL:
            session = AiohttpSession(proxy=PROXY_URL)
            self.bot = Bot(token=token, session=session)
        else:
            self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self._task: Optional[asyncio.Task] = None
        self._register_handlers()

    def _register_handlers(self):
        @self.dp.message()
        async def handle_user_message(message: types.Message):
            if message.text and message.text.startswith("/"):
                if message.text.lower() == "/start":
                    await message.answer(
                        "👋 Здравствуйте! Пожалуйста, опишите вашу проблему или задайте вопрос.\n\n"
                        "Ваше сообщение будет передано в поддержку.",
                        parse_mode="HTML"
                    )
                return

            target_chat_id = await self.manager.get_notification_target(self.owner_id)

            user_info = (
                f"📩 Новое обращение из @{self.username}\n\n"
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
                    forwarded_msg = await self.manager.main_bot.send_photo(
                        chat_id=target_chat_id,
                        photo=message.photo[-1].file_id,
                        caption=caption,
                        parse_mode="HTML"
                    )
                elif message.text:
                    full_text = f"{user_info}\n\n💬 Сообщение:\n{message.text}"
                    forwarded_msg = await self.manager.main_bot.send_message(
                        chat_id=target_chat_id,
                        text=full_text[:4096],
                        parse_mode="HTML"
                    )
                elif message.video:
                    caption = f"{user_info}\n\n🎥 Видео"
                    if message.caption:
                        caption += f"\n\n💬 Текст к видео:\n{message.caption}"
                    forwarded_msg = await self.manager.main_bot.send_video(
                        chat_id=target_chat_id,
                        video=message.video.file_id,
                        caption=caption[:1024],
                        parse_mode="HTML"
                    )
                elif message.document:
                    caption = f"{user_info}\n\n📄 Документ"
                    if message.caption:
                        caption += f"\n\n💬 Текст к документу:\n{message.caption}"
                    forwarded_msg = await self.manager.main_bot.send_document(
                        chat_id=target_chat_id,
                        document=message.document.file_id,
                        caption=caption[:1024],
                        parse_mode="HTML"
                    )
                elif message.audio:
                    caption = f"{user_info}\n\n🎵 Аудио"
                    if message.caption:
                        caption += f"\n\n💬 Текст к аудио:\n{message.caption}"
                    forwarded_msg = await self.manager.main_bot.send_audio(
                        chat_id=target_chat_id,
                        audio=message.audio.file_id,
                        caption=caption[:1024],
                        parse_mode="HTML"
                    )
                elif message.voice:
                    caption = f"{user_info}\n\n🎤 Голосовое сообщение"
                    if message.caption:
                        caption += f"\n\n💬 Текст к голосовому:\n{message.caption}"
                    forwarded_msg = await self.manager.main_bot.send_voice(
                        chat_id=target_chat_id,
                        voice=message.voice.file_id,
                        caption=caption[:1024],
                        parse_mode="HTML"
                    )
                elif message.video_note:
                    text = f"{user_info}\n\n🎬 Видеосообщение (кружок)"
                    forwarded_msg = await self.manager.main_bot.send_message(
                        chat_id=target_chat_id,
                        text=text,
                        parse_mode="HTML"
                    )
                    await self.manager.main_bot.send_video_note(
                        chat_id=target_chat_id,
                        video_note=message.video_note.file_id
                    )
                elif message.animation:
                    caption = f"{user_info}\n\n🎬 GIF-анимация"
                    if message.caption:
                        caption += f"\n\n💬 Текст к GIF:\n{message.caption}"
                    forwarded_msg = await self.manager.main_bot.send_animation(
                        chat_id=target_chat_id,
                        animation=message.animation.file_id,
                        caption=caption[:1024],
                        parse_mode="HTML"
                    )
                elif message.sticker:
                    text = f"{user_info}\n\n🏷️ Стикер"
                    forwarded_msg = await self.manager.main_bot.send_message(
                        chat_id=target_chat_id,
                        text=text,
                        parse_mode="HTML"
                    )
                    await self.manager.main_bot.send_sticker(
                        chat_id=target_chat_id,
                        sticker=message.sticker.file_id
                    )
                elif message.contact:
                    text = (
                        f"{user_info}\n\n📇 Контакт\n"
                        f"Имя: {message.contact.first_name}\n"
                        f"Телефон: {message.contact.phone_number}"
                    )
                    forwarded_msg = await self.manager.main_bot.send_message(
                        chat_id=target_chat_id,
                        text=text[:4096],
                        parse_mode="HTML"
                    )
                elif message.location:
                    text = (
                        f"{user_info}\n\n📍 Геопозиция\n"
                        f"Широта: {message.location.latitude}\n"
                        f"Долгота: {message.location.longitude}"
                    )
                    forwarded_msg = await self.manager.main_bot.send_message(
                        chat_id=target_chat_id,
                        text=text[:4096],
                        parse_mode="HTML"
                    )
                elif message.poll:
                    text = f"{user_info}\n\n📊 Опрос: {message.poll.question}"
                    forwarded_msg = await self.manager.main_bot.send_message(
                        chat_id=target_chat_id,
                        text=text[:4096],
                        parse_mode="HTML"
                    )
                else:
                    forwarded_msg = await self.manager.main_bot.send_message(
                        chat_id=target_chat_id,
                        text=f"{user_info}\n\n⚠️ Неподдерживаемый тип: {message.content_type}",
                        parse_mode="HTML"
                    )

                if forwarded_msg:
                    self.manager.forwarded_message_map[(target_chat_id, forwarded_msg.message_id)] = (
                        message.from_user.id,
                        self.token,
                    )

                await message.answer("✅ Сообщение отправлено в поддержку!", parse_mode="HTML")

            except Exception as e:
                logger.error(f"Ошибка пересылки от @{self.username}: {e}", exc_info=True)
                await message.answer("❌ Не удалось отправить сообщение. Попробуйте позже.", parse_mode="HTML")

    async def start_polling(self):
        try:
            await self.dp.start_polling(self.bot, handle_signals=False)
        except asyncio.CancelledError:
            logger.info(f"Polling для @{self.username} отменён")
            raise
        except Exception as e:
            logger.exception(f"Ошибка в polling для @{self.username}: {e}")
        finally:
            await self.bot.session.close()
            logger.info(f"Сессия бота @{self.username} закрыта")

    async def stop(self):
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                logger.error(f"Ошибка при остановке @{self.username}: {e}")

    def set_task(self, task: asyncio.Task):
        self._task = task

class BotManager:
    def __init__(self, main_bot: Bot, db):
        self.main_bot = main_bot
        self.db = db
        self.active_instances: Dict[str, BotInstance] = {}
        self.forwarded_message_map: Dict[Tuple[int, int], Tuple[int, str]] = {}

    async def get_notification_target(self, owner_id: int) -> int:
        return await self.db.get_notification_target(owner_id)

    async def set_notification_target(self, owner_id: int, chat_id: int):
        await self.db.set_notification_target(owner_id, chat_id)

    async def register_bot(self, token: str, owner_id: int, bot_username: str):
        if token in self.active_instances:
            raise ValueError("Токен уже используется")
        instance = BotInstance(token, owner_id, bot_username, self)
        task = asyncio.create_task(instance.start_polling(), name=f"bot_{bot_username}")
        instance.set_task(task)
        self.active_instances[token] = instance
        logger.info(f"Бот @{bot_username} запущен (токен {token[:8]}...)")

    async def shutdown_bot(self, token: str):
        instance = self.active_instances.get(token)
        if not instance:
            return
        await instance.stop()
        del self.active_instances[token]
        logger.info(f"Бот @{instance.username} остановлен и удалён")

    async def shutdown_all(self):
        if not self.active_instances:
            return
        tokens = list(self.active_instances.keys())
        logger.info(f"Останавливаем {len(tokens)} дочерних ботов...")
        shutdown_tasks = [self.active_instances[token].stop() for token in tokens]
        if shutdown_tasks:
            results = await asyncio.gather(*shutdown_tasks, return_exceptions=True)
            for i, res in enumerate(results):
                if isinstance(res, Exception) and not isinstance(res, asyncio.CancelledError):
                    logger.error(f"Ошибка при остановке бота: {res}")
        self.active_instances.clear()
        self.forwarded_message_map.clear()
        logger.info("Все дочерние боты остановлены")