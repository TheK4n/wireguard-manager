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


def check_admin(message_from_user_id) -> bool:
    return message_from_user_id == int(os.getenv("ADMIN"))


def check_args(message_text) -> bool:
    return len(message_text.split(" ")) > 1


def base_handler(message, command: str):
    logger.info(f"'{message.text}' executed from {message.from_user.username}:{message.from_user.id}")
    if not check_admin(message.from_user.id):
        return
    if not check_args(message.text):
        bot.reply_to(message, "Client name was not defined")
        return

    first_message = bot.reply_to(message, "Please wait!")

    client_name = message.text.split()[1]
    command_result = execute_sh("wg_manager.sh", command, client_name)

    if command_result.returncode:
        logger.error(command_result.stderr.decode().strip())
        bot.edit_message_text(chat_id=first_message.chat.id, message_id=first_message.message_id, text="Error!")
        return
    photo = BytesIO(command_result.stdout)
    photo.seek(0)
    bot.send_photo(message.chat.id, photo=photo)
    bot.delete_message(chat_id=first_message.chat.id, message_id=first_message.message_id)


@bot.message_handler(commands=['add'])
def add_client_handler(message):
    base_handler(message, "add_tg")


@bot.message_handler(commands=['get_text'])
def get_text_handler(message):
    logger.info(f"'{message.text}' executed from {message.from_user.username}:{message.from_user.id}")
    if not check_admin(message.from_user.id):
        return
    if not check_args(message.text):
        bot.reply_to(message, "Client name was not defined")
        return

    first_message = bot.reply_to(message, "Please wait!")

    client_name = message.text.split()[1]
    command_result = execute_sh("wg_manager.sh", "get_file", client_name)

    if command_result.returncode:
        logger.error(command_result.stderr.decode().strip())
        bot.edit_message_text(chat_id=first_message.chat.id, message_id=first_message.message_id, text="Error!")
        return

    bot.reply_to(message, "```" + command_result.stdout.decode() + "```")
    bot.delete_message(chat_id=first_message.chat.id, message_id=first_message.message_id)


@bot.message_handler(commands=['get_file'])
def get_file_handler(message):
    logger.info(f"'{message.text}' executed from {message.from_user.username}:{message.from_user.id}")
    if not check_admin(message.from_user.id):
        return
    if not check_args(message.text):
        bot.reply_to(message, "Client name was not defined")
        return

    first_message = bot.reply_to(message, "Please wait!")

    client_name = message.text.split()[1]
    command_result = execute_sh("wg_manager.sh", "get_file", client_name)

    if command_result.returncode:
        logger.error(command_result.stderr.decode().strip())
        bot.edit_message_text(chat_id=first_message.chat.id, message_id=first_message.message_id, text="Error!")
        return

    file = BytesIO(command_result.stdout)
    file.name = client_name + ".conf"
    file.seek(0)
    bot.send_document(message.chat.id, document=file)
    bot.delete_message(chat_id=first_message.chat.id, message_id=first_message.message_id)


@bot.message_handler(commands=['get'])
def get_client_handler(message):
    base_handler(message, "get_tg")


@bot.message_handler(commands=['ls'])
def ls_client_handler(message):
    logger.info(f"'{message.text}' executed from {message.from_user.username}:{message.from_user.id}")
    if not check_admin(message.from_user.id):
        return

    command_result = execute_sh("wg_manager.sh", "ls", "")

    if command_result.returncode:
        logger.error(command_result.stderr.decode().strip())
        bot.reply_to(message, "Error")
        return

    bot.reply_to(message, command_result.stdout.decode())


@bot.message_handler(commands=['rm'])
def get_client_handler(message):
    logger.info(f"'{message.text}' executed from {message.from_user.username}:{message.from_user.id}")
    if not check_admin(message.from_user.id):
        return

    if not check_args(message.text):
        bot.reply_to(message, "Client name was not defined")
        return

    first_message = bot.reply_to(message, "Please wait!")

    client_name = message.text.split()[1]
    command_result = execute_sh("wg_manager.sh", "rm", client_name)

    if command_result.returncode:
        logger.error(command_result.stderr.decode().strip())
        bot.reply_to(message, "Error")
        return

    bot.delete_message(chat_id=first_message.chat.id, message_id=first_message.message_id)


if __name__ == "__main__":
    logger.info("Bot started")
    bot.infinity_polling()
    logger.info("Bot stopped")
