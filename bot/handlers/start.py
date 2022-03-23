from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp, Command

from loader import dp, logger
from data import ADMINS
from keyboards import menu


@dp.message_handler(CommandStart(), state='*', user_id=ADMINS)
async def bot_start(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    logger.info(f"{message.text} from user {message.from_user.username}:{message.from_user.id}")
    await message.answer(f"Hello, Access allowed to {message.from_user.full_name}", reply_markup=menu)


@dp.message_handler(CommandHelp(), state='*', user_id=ADMINS)
async def bot_help(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await message.answer("WireGuard Manager bot\n\nGithub: https://github.com/thek4n/wireguard-manager")


@dp.message_handler(Command("menu"), state='*', user_id=ADMINS)
async def bot_menu(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await message.answer("WireGuard Manager bot menu", reply_markup=menu)
