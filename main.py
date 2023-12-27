import telebot
import random
from config import TELEGRAM_API_TOKEN
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_kawaii_instructions(message):
    instructions = (
        "Konnichiwa~! To make your message kawaii, simply type /kawaii followed by your message. "
        "For example: /kawaii Hello, how are you? UwU"
    )
    bot.reply_to(message, instructions)


@bot.message_handler(commands=['kawaii'])
def kawaii_command(message):
    command_parts = message.text.split(' ', 1)
    if len(command_parts) > 1:
        user_message = command_parts[1].strip()
        kawaii_message = make_kawaii(user_message)
        bot.reply_to(message, kawaii_message)
    else:
        bot.reply_to(message, "Nya~! Please provide a message after the /kawaii command. UwU")


def make_kawaii(user_message):
    string_list = ["Nya!", "OwO", "UwU", ":3"]
    random_string = random.choice(string_list)
    kawaii_message = user_message + " " + random_string
    return kawaii_message

bot.polling(none_stop=True, interval=0)
