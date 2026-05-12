TEXTS = {
    "ru": {
        "start": (
            "👋 <b>Добро пожаловать в SupportBridge!</b>\n\n"
            "Я помогаю создавать ботов для поддержки и перенаправлять "
            "обращения пользователей в удобное для вас место.\n\n"
            "📌 <b>Что я умею:</b>\n"
            "• Создавать ботов поддержки\n"
            "• Привязывать чаты для получения обращений\n"
            "• Пересылать сообщения от пользователей"
        ),
        "help": (
            "📖 <b>Команды и кнопки:</b>\n\n"
            "/start — главное меню\n"
            "/help — эта справка\n\n"
            "🔘 <b>Кнопки в меню:</b>\n"
            "• 📬 Получать сюда — привязать текущий чат\n"
            "• 🔗 Привязать чат — указать ID другого чата\n"
            "• 🤖 Создать бота поддержки — добавить нового бота\n"
            "• ℹ️ Статус — информация о ваших ботах"
        ),
        "btn_notify_here": "📬 Получать сюда",
        "btn_bind_chat": "🔗 Привязать чат",
        "btn_create_bot": "🤖 Создать бота поддержки",
        "btn_status": "ℹ️ Статус",
        "btn_back": "🔙 Назад",
        "notify_here_success_ls": "✅ <b>Готово!</b>\nТеперь все обращения будут приходить вам в личные сообщения.",
        "notify_here_success_chat": "✅ <b>Чат успешно привязан!</b>\n\n📢 Все обращения будут приходить в этот чат.\n🆔 ID чата: <code>{chat_id}</code>",
        "notify_here_error_not_member": "❌ <b>Бот не добавлен в этот чат</b>\n\nСначала добавьте бота в чат, затем нажмите кнопку снова.",
        "bind_chat_prompt": (
            "🔗 <b>Привязка другого чата</b>\n\n"
            "Пожалуйста, отправьте <b>ID чата или канала</b>, "
            "куда должны приходить обращения.\n\n"
            "ℹ️ <b>Как получить ID:</b>\n"
            "• Для канала/группы: добавьте бота @IDCollectors_bot\n"
            "• ID должен быть числом (например: <code>-1001234567890</code>)"
        ),
        "bind_chat_error_wrong_place": (
            "❌ <b>Неверное действие</b>\n\n"
            "Эта кнопка предназначена для привязки <b>другого</b> чата "
            "из личных сообщений.\n\n"
            "Чтобы привязать <b>этот</b> чат, используйте кнопку "
            "«📬 Получать сюда»."
        ),
        "create_bot_prompt": (
            "🤖 <b>Создание бота поддержки</b>\n\n"
            "Пожалуйста, пришлите токен вашего Telegram-бота.\n\n"
            "🔑 <b>Как получить токен:</b>\n"
            "1. Найдите @BotFather в Telegram\n"
            "2. Отправьте команду /newbot\n"
            "3. Следуйте инструкциям\n"
            "4. Скопируйте полученный токен\n\n"
            "📝 <b>Пример токена:</b>\n"
            "<code>8763200231:g261RIR60IAbGgQTxuJ8S2xEIFFXdG044s</code>"
        ),
        "status_header": "📊 <b>Статистика</b>\n\n",
        "status_no_bots": "ℹ️ <b>У вас пока нет активных ботов</b>\n\nЧтобы начать, нажмите «🤖 Создать бота для принятия сообщений» в главном меню.",
        "status_target_ls": "📬 в ваши личные сообщения",
        "status_target_chat": "📬 в чат с ID: <code>{chat_id}</code>",
        "status_bots_count": "🤖 Активных ботов: <b>{count}</b>\n",
        "status_bots_list": "<b>📋 Список ботов:</b>\n",
        "status_bot_line": "• @{username} (<code>{token}</code>)\n",
        "create_bot_success": (
            "✅ <b>Бот успешно создан!</b>\n\n"
            "🤖 Имя: @{username}\n"
            "{location}\n\n"
            "Теперь все сообщения пользователей будут автоматически "
            "пересылаться в указанное место."
        ),
        "create_bot_token_used": "❌ <b>Токен уже используется</b>\n\nЭтот токен уже зарегистрирован в системе.",
        "create_bot_invalid_token": "❌ Неверный токен бота. Проверьте правильность токена.",
        "create_bot_error": "❌ Ошибка подключения: {error}",
        "location_ls": "📬 вам в личные сообщения",
        "location_chat": "📬 в чат (ID: <code>{chat_id}</code>)",
        "admin_reply_text": "📨 <b>Ответ от поддержки:</b>\n\n{text}",
        "admin_reply_photo": "📸 <b>Ответ от поддержки (фото)</b>",
        "admin_reply_photo_caption": "📸 <b>Ответ от поддержки (фото):</b>\n\n{caption}",
        "admin_reply_video": "🎥 <b>Ответ от поддержки (видео)</b>",
        "admin_reply_video_caption": "🎥 <b>Ответ от поддержки (видео):</b>\n\n{caption}",
        "admin_reply_document": "📎 <b>Ответ от поддержки (документ)</b>",
        "admin_reply_document_caption": "📎 <b>Ответ от поддержки (документ):</b>\n\n{caption}",
        "admin_reply_audio": "🎵 <b>Ответ от поддержки (аудио)</b>",
        "admin_reply_audio_caption": "🎵 <b>Ответ от поддержки (аудио):</b>\n\n{caption}",
        "admin_reply_voice": "🎤 <b>Ответ от поддержки (голосовое)</b>",
        "admin_reply_voice_caption": "🎤 <b>Ответ от поддержки (голосовое):</b>\n\n{caption}",
        "admin_reply_animation": "🎬 <b>Ответ от поддержки (GIF)</b>",
        "admin_reply_animation_caption": "🎬 <b>Ответ от поддержки (GIF):</b>\n\n{caption}",
        "reply_success_text": "✅ Текстовый ответ отправлен пользователю.",
        "reply_success_sticker": "✅ Стикер отправлен пользователю.",
        "reply_success_photo": "✅ Фото отправлено пользователю.",
        "reply_success_video": "✅ Видео отправлено пользователю.",
        "reply_success_document": "✅ Документ отправлен пользователю.",
        "reply_success_audio": "✅ Аудио отправлено пользователю.",
        "reply_success_voice": "✅ Голосовое сообщение отправлено пользователю.",
        "reply_success_video_note": "✅ Видеосообщение отправлено пользователю.",
        "reply_success_animation": "✅ GIF отправлен пользователю.",
        "reply_error_bot_inactive": "❌ <b>Бот отключён</b>\n\nБот, через который пришло обращение, больше не активен.",
        "reply_error_unsupported": "⚠️ <b>Неподдерживаемый тип контента</b>\n\nТип: {type}",
        "reply_error_file_too_big": "❌ Файл слишком большой для отправки через Telegram.",
        "reply_error_wrong_file_id": "❌ Не удалось обработать файл. Возможно, он устарел.",
        "reply_error_chat_not_found": "❌ Пользователь заблокировал бота или удалил чат.",
        "reply_error_unknown": "❌ <b>Ошибка при отправке ответа</b>\n\n{error}",
        "invalid_chat_id_format": "❌ <b>Неверный формат</b>\n\nID должен быть целым числом.\nПример: <code>-1001234567890</code>",
        "chat_bind_success": "✅ <b>Чат успешно привязан!</b>\n\n🆔 ID: <code>{chat_id}</code>\n📬 Все обращения будут приходить сюда.",
        "chat_bind_error_not_member": "❌ <b>Бот не в чате</b>\n\nСначала добавьте бота в указанный чат, затем повторите попытку.",
        "chat_bind_not_found": "❌ <b>Чат не найден</b>\n\nПроверьте правильность ID и что бот добавлен в чат.",
        "chat_bind_error": "❌ <b>Ошибка при проверке чата</b>\n\n{error}",
    },
    "en": {
        "start": (
            "👋 <b>Welcome to SupportBridge!</b>\n\n"
            "I help create support bots and forward "
            "user requests to a convenient place.\n\n"
            "📌 <b>What I can do:</b>\n"
            "• Create support bots\n"
            "• Bind chats to receive requests\n"
            "• Forward messages from users"
        ),
        "help": (
            "📖 <b>Commands and buttons:</b>\n\n"
            "/start — main menu\n"
            "/help — this help\n\n"
            "🔘 <b>Menu buttons:</b>\n"
            "• 📬 Receive here — bind current chat\n"
            "• 🔗 Bind chat — specify another chat ID\n"
            "• 🤖 Create support bot — add a new bot\n"
            "• ℹ️ Status — info about your bots"
        ),
        "btn_notify_here": "📬 Receive here",
        "btn_bind_chat": "🔗 Bind chat",
        "btn_create_bot": "🤖 Create support bot",
        "btn_status": "ℹ️ Status",
        "btn_back": "🔙 Back",
        "notify_here_success_ls": "✅ <b>Done!</b>\nAll requests will now come to your personal messages.",
        "notify_here_success_chat": "✅ <b>Chat successfully bound!</b>\n\n📢 All requests will come to this chat.\n🆔 Chat ID: <code>{chat_id}</code>",
        "notify_here_error_not_member": "❌ <b>Bot is not added to this chat</b>\n\nAdd the bot to the chat first, then press the button again.",
        "bind_chat_prompt": (
            "🔗 <b>Bind another chat</b>\n\n"
            "Please send the <b>chat or channel ID</b> "
            "where requests should come.\n\n"
            "ℹ️ <b>How to get ID:</b>\n"
            "• For channel/group: add @IDCollectors_bot\n"
            "• ID must be a number (e.g., <code>-1001234567890</code>)"
        ),
        "bind_chat_error_wrong_place": (
            "❌ <b>Invalid action</b>\n\n"
            "This button is for binding <b>another</b> chat "
            "from private messages.\n\n"
            "To bind <b>this</b> chat, use the "
            "«📬 Receive here» button."
        ),
        "create_bot_prompt": (
            "🤖 <b>Create support bot</b>\n\n"
            "Please send your Telegram bot token.\n\n"
            "🔑 <b>How to get a token:</b>\n"
            "1. Find @BotFather on Telegram\n"
            "2. Send /newbot command\n"
            "3. Follow the instructions\n"
            "4. Copy the received token\n\n"
            "📝 <b>Example token:</b>\n"
            "<code>8763200231:g261RIR60IAbGgQTxuJ8S2xEIFFXdG044s</code>"
        ),
        "status_header": "📊 <b>Statistics</b>\n\n",
        "status_no_bots": "ℹ️ <b>You have no active bots yet</b>\n\nTo start, click «🤖 Create support bot» in the main menu.",
        "status_target_ls": "📬 to your personal messages",
        "status_target_chat": "📬 to chat with ID: <code>{chat_id}</code>",
        "status_bots_count": "🤖 Active bots: <b>{count}</b>\n",
        "status_bots_list": "<b>📋 Bot list:</b>\n",
        "status_bot_line": "• @{username} (<code>{token}</code>)\n",
        "create_bot_success": (
            "✅ <b>Bot successfully created!</b>\n\n"
            "🤖 Name: @{username}\n"
            "{location}\n\n"
            "All user messages will now be automatically "
            "forwarded to the specified location."
        ),
        "create_bot_token_used": "❌ <b>Token already in use</b>\n\nThis token is already registered in the system.",
        "create_bot_invalid_token": "❌ Invalid bot token. Please check the token.",
        "create_bot_error": "❌ Connection error: {error}",
        "location_ls": "📬 to your personal messages",
        "location_chat": "📬 to chat (ID: <code>{chat_id}</code>)",
        "admin_reply_text": "📨 <b>Support reply:</b>\n\n{text}",
        "admin_reply_photo": "📸 <b>Support reply (photo)</b>",
        "admin_reply_photo_caption": "📸 <b>Support reply (photo):</b>\n\n{caption}",
        "admin_reply_video": "🎥 <b>Support reply (video)</b>",
        "admin_reply_video_caption": "🎥 <b>Support reply (video):</b>\n\n{caption}",
        "admin_reply_document": "📎 <b>Support reply (document)</b>",
        "admin_reply_document_caption": "📎 <b>Support reply (document):</b>\n\n{caption}",
        "admin_reply_audio": "🎵 <b>Support reply (audio)</b>",
        "admin_reply_audio_caption": "🎵 <b>Support reply (audio):</b>\n\n{caption}",
        "admin_reply_voice": "🎤 <b>Support reply (voice)</b>",
        "admin_reply_voice_caption": "🎤 <b>Support reply (voice):</b>\n\n{caption}",
        "admin_reply_animation": "🎬 <b>Support reply (GIF)</b>",
        "admin_reply_animation_caption": "🎬 <b>Support reply (GIF):</b>\n\n{caption}",
        "reply_success_text": "✅ Text response sent to user.",
        "reply_success_sticker": "✅ Sticker sent to user.",
        "reply_success_photo": "✅ Photo sent to user.",
        "reply_success_video": "✅ Video sent to user.",
        "reply_success_document": "✅ Document sent to user.",
        "reply_success_audio": "✅ Audio sent to user.",
        "reply_success_voice": "✅ Voice message sent to user.",
        "reply_success_video_note": "✅ Video note sent to user.",
        "reply_success_animation": "✅ GIF sent to user.",
        "reply_error_bot_inactive": "❌ <b>Bot disabled</b>\n\nThe bot that received the request is no longer active.",
        "reply_error_unsupported": "⚠️ <b>Unsupported content type</b>\n\nType: {type}",
        "reply_error_file_too_big": "❌ File is too large to send via Telegram.",
        "reply_error_wrong_file_id": "❌ Failed to process the file. It may be outdated.",
        "reply_error_chat_not_found": "❌ User has blocked the bot or deleted the chat.",
        "reply_error_unknown": "❌ <b>Error sending reply</b>\n\n{error}",
        "invalid_chat_id_format": "❌ <b>Invalid format</b>\n\nID must be an integer.\nExample: <code>-1001234567890</code>",
        "chat_bind_success": "✅ <b>Chat successfully bound!</b>\n\n🆔 ID: <code>{chat_id}</code>\n📬 All requests will come here.",
        "chat_bind_error_not_member": "❌ <b>Bot is not in the chat</b>\n\nAdd the bot to the specified chat first, then try again.",
        "chat_bind_not_found": "❌ <b>Chat not found</b>\n\nCheck the ID and make sure the bot is added to the chat.",
        "chat_bind_error": "❌ <b>Error checking chat</b>\n\n{error}",
    }
}