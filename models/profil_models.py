from aiogram.dispatcher.filters.state import State, StatesGroup




class ProfileStatesGroup(StatesGroup):

    photo = State()
    name = State()
    age = State()
    description = State()

