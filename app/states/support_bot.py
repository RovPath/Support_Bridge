from aiogram.fsm.state import State, StatesGroup

class SupportBotStates(StatesGroup):
    waiting_for_token = State()
    waiting_for_chat_id = State()