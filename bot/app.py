import asyncio

from aiogram import executor, types
from loader import dp
import handlers


async def set_default_commands(dispatcher):
    await dispatcher.bot.set_my_commands(
        [
            types.BotCommand("start", "Start bot"),
            types.BotCommand("menu", "Menu"),
            types.BotCommand("help", "Help"),
        ]
    )


async def on_startup(dispatcher):
    await asyncio.sleep(1)

    await set_default_commands(dispatcher)


async def on_shutdown(dispatcher):
    await dispatcher.close()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)