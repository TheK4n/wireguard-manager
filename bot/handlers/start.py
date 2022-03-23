from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp, Command

from loader import dp, logger
from data import ADMINS, MESSAGES
from keyboards import menu


@dp.message_handler(CommandStart(), state='*', user_id=ADMINS)
async def bot_start(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    logger.info(f"{message.text} from user {message.from_user.username}:{message.from_user.id}")
    await message.answer(MESSAGES["START"].format(name=message.from_user.full_name), reply_markup=menu)


@dp.message_handler(CommandHelp(), state='*', user_id=ADMINS)
async def bot_help(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await message.answer(MESSAGES["HELP"])


@dp.message_handler(Command("menu"), state='*', user_id=ADMINS)
async def bot_menu(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await message.answer(MESSAGES["MENU"], reply_markup=menu)
