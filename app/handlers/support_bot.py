import logging
from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError
from aiogram.client.session.aiohttp import AiohttpSession
from app.states.support_bot import SupportBotStates
from app.utils.texts import TEXTS
from app.middlewares.bot_manager import BotManager
from config import USE_PROXY, PROXY_URL

logger = logging.getLogger(__name__)
router = Router()

@router.callback_query(F.data == "create_support_bot")
async def create_support(
    callback: types.CallbackQuery,
    state: FSMContext,
    lang: str
):
    t = TEXTS.get(lang, TEXTS["ru"])
    await callback.message.edit_text(
        t["create_bot_prompt"],
        parse_mode="HTML"
    )
    await state.set_state(SupportBotStates.waiting_for_token)
    await callback.answer()

@router.message(SupportBotStates.waiting_for_token)
async def process_bot_token(
    message: types.Message,
    state: FSMContext,
    bot_manager: BotManager,
    lang: str
):
    t = TEXTS.get(lang, TEXTS["ru"])
    token = message.text.strip()
    owner_id = message.from_user.id

    try:
        if USE_PROXY and PROXY_URL:
            session = AiohttpSession(proxy=PROXY_URL)
            test_bot = Bot(token=token, session=session)
        else:
            test_bot = Bot(token=token)
        bot_info = await test_bot.get_me()
        bot_username = bot_info.username
        await test_bot.session.close()

        await bot_manager.register_bot(token, owner_id, bot_username)

        target_chat_id = await bot_manager.get_notification_target(owner_id)
        if target_chat_id == owner_id:
            location = t["location_ls"]
        else:
            location = t["location_chat"].format(chat_id=target_chat_id)

        await message.answer(
            t["create_bot_success"].format(username=bot_username, location=location),
            parse_mode="HTML"
        )
        logger.info(f"Бот @{bot_username} привязан к владельцу {owner_id}")

    except ValueError:
        await message.answer(t["create_bot_token_used"], parse_mode="HTML")
    except TelegramAPIError as e:
        if "401" in str(e):
            await message.answer(t["create_bot_invalid_token"], parse_mode="HTML")
        else:
            await message.answer(t["create_bot_error"].format(error=str(e)), parse_mode="HTML")
        logger.error(f"Ошибка регистрации токена {token[:8]}... : {e}")
    except Exception as e:
        await message.answer(f"❌ <b>Неожиданная ошибка</b>\n\n{str(e)}", parse_mode="HTML")
        logger.exception("Критическая ошибка при регистрации бота")
    finally:
        await state.clear()