from aiogram.fsm.state import State, StatesGroup


class SupportBotRegistration(StatesGroup):
    waiting_for_token = State()
