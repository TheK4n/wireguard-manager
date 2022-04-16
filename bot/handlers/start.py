from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp, Command

from loader import dp, logger
from data import ADMINS, Text
from keyboards import menu


async def base_handler(message: types.Message, answer_text: str, **kwargs):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    logger.info(f"{message.text} from user {message.from_user.username}:{message.from_user.id}")
    await message.answer(answer_text, **kwargs)


@dp.message_handler(CommandStart(), state='*', user_id=ADMINS)
async def bot_start(message: types.Message):
    await base_handler(message, Text.START.format(name=message.from_user.full_name), reply_markup=menu)


@dp.message_handler(CommandHelp(), state='*', user_id=ADMINS)
async def bot_help(message: types.Message):
    await base_handler(message, Text.HELP)


@dp.message_handler(Command("menu"), state='*', user_id=ADMINS)
async def bot_menu(message: types.Message):
    await base_handler(message, Text.MENU, reply_markup=menu)
