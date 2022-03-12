import datetime
import os
import subprocess
import telebot
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))


@bot.message_handler(commands=['add_client'])
def send_welcome(message):
    print(message.from_user)
    if message.from_user.id == int(os.getenv("ADMIN")):
        bot.reply_to(message, "Please wait!")

        command_output = subprocess.run(["bash", os.getenv("EXECPATH")],
                                        capture_output=True)
        print(command_output)

        bot.reply_to(message, command_output.stdout.decode())
        print(datetime.datetime.now(), "New client was added")


if __name__ == "__main__":
    bot.infinity_polling()
