import os
import subprocess
import telebot
from dotenv import load_dotenv
from loguru import logger


logger.add("wg_manager.log", format="{time} {level} {message}", level="DEBUG", rotation="20 MB", compression="gz")
load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))


def execute_add_client_sh(path: str, client_name: str):
    return subprocess.run(["bash", path, client_name], capture_output=True)


@bot.message_handler(commands=['add_client'])
def add_client_handler(message):
    if message.from_user.id != int(os.getenv("ADMIN")):
        return

    message_args = message.text.split(" ")
    if len(message_args) < 2:
        bot.reply_to(message, "Client name was not defined, use '/add_client <client_name>'")
        return

    bot.reply_to(message, "Please wait!")

    client_name = message_args[1]
    command_add_client_result = execute_add_client_sh(os.getenv("EXECPATH"), client_name)

    if command_add_client_result.returncode:
        logger.error("add_client.sh returned non-zero code")
        bot.reply_to(message, "Error")
        return

    bot.reply_to(message, command_add_client_result.stdout.decode())
    logger.info(f"New client '{client_name}' was added")


if __name__ == "__main__":
    logger.info("Bot started")
    bot.infinity_polling()
    logger.info("Bot stopped")