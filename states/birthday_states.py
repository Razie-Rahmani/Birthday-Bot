from aiogram.fsm.state import State, StatesGroup


class BirthdayForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_birthday = State()