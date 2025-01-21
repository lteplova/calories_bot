from aiogram.fsm.state import State, StatesGroup
class Form(StatesGroup):
    weight = State()
    height = State()
    age = State()
    gender = State()
    minutes = State()
    city = State()
    water_add = State()
    food_weight = State()

