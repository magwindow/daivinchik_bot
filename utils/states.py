from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    name = State()
    age = State()
    city = State()
    gender = State()
    look_for = State()
    bio = State()
    photo = State()
    