from aiogram.fsm.state import State, StatesGroup


class SupportBotRegistration(StatesGroup):
    waiting_for_token = State()


class ChatBinding(StatesGroup):
    waiting_for_chat_id = State()
