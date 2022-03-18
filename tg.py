import os
import subprocess
import telebot
from dotenv import load_dotenv
from loguru import logger
from io import BytesIO


logger.add("wg_manager.log", format="{time} {level} {message}", level="DEBUG", rotation="20 MB", compression="gz")
load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))


def execute_sh(path: str, command: str, client_name: str):
    return subprocess.run(["bash", path, command, client_name], capture_output=True)


@bot.message_handler(commands=['add'])
def add_client_handler(message):
    if message.from_user.id != int(os.getenv("ADMIN")):
        return

    message_args = message.text.split(" ")
    if len(message_args) < 2:
        bot.reply_to(message, "Client name was not defined, use '/add_client <client_name>'")
        return

    bot.reply_to(message, "Please wait!")

    client_name = message_args[1]
    command_result = execute_sh("wg_manager.sh", "add_tg", client_name)

    if command_result.returncode:
        logger.error("add_client.sh returned non-zero code")
        bot.reply_to(message, "Error")
        return
    photo = BytesIO(command_result.stdout)
    photo.seek(0)
    bot.send_photo(message.chat.id, photo=photo)
    logger.info(f"New client '{client_name}' was added")


@bot.message_handler(commands=['get'])
def get_client_handler(message):
    if message.from_user.id != int(os.getenv("ADMIN")):
        return

    message_args = message.text.split(" ")
    if len(message_args) < 2:
        bot.reply_to(message, "Client name was not defined, use '/get_client <client_name>'")
        return

    bot.reply_to(message, "Please wait!")

    client_name = message_args[1]
    command_result = execute_sh("wg_manager.sh", "get_client_qrcode", client_name)

    if command_result.returncode:
        logger.error("get_client.sh returned non-zero code")
        bot.reply_to(message, "Error")
        return

    photo = BytesIO(command_result.stdout)
    photo.seek(0)
    bot.send_photo(message.chat.id, photo=photo)


if __name__ == "__main__":
    logger.info("Bot started")
    bot.infinity_polling()
    logger.info("Bot stopped")
