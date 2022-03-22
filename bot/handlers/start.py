from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp, Command

from loader import dp
from data import ADMINS

from keyboards import menu


@dp.message_handler(CommandStart(), user_id=ADMINS)
async def bot_start(message: types.Message):
    await message.answer(f"Hello, Access allowed to {message.from_user.full_name}", reply_markup=menu)


@dp.message_handler(CommandHelp(), user_id=ADMINS)
async def bot_start(message: types.Message):
    await message.answer("Help")


@dp.message_handler(Command("menu"), user_id=ADMINS)
async def bot_start(message: types.Message):
    await message.answer("WireGuard Manager bot menu", reply_markup=menu)
