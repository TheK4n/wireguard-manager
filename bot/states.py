from aiogram.dispatcher.filters.state import StatesGroup, State


class GetClient(StatesGroup):
    name = State()
    choice = State()
    del_confirm = State()


class AddClient(StatesGroup):
    name = State()
