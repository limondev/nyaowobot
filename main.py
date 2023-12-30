import telebot
import random
import requests


from config import TELEGRAM_API_TOKEN, api_key
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_kawaii_instructions(message):
    instructions = (
        "Konnichiwa~! To make your message kawaii, simply type /kawaii followed by your message. "
        "For example: /kawaii Hello, how are you? UwU"
        "Also, U can ask this bot for weather in your city, just type /weather followed by mane of your city :3"
        "For example: /weather Kharkiv"
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


def make_kawaii(user_message: str):
    string_list = ["Nya!", "OwO", "UwU", ":3"]
    random_string = random.choice(string_list)
    if random_string in ["UwU", "OwO"]:
        user_message = user_message.replace("s", "w")
        user_message = user_message.replace("l", "w")
        user_message = user_message.replace("r", "w")
        user_message = user_message.replace("x", "w")
    kawaii_message = user_message + " " + random_string
    return kawaii_message

@bot.message_handler(commands=['weather'])
def get_weather(message):
    try:
        city = message.text.split('/weather ', 1)[1]
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(url)
        weather_data = response.json()

        if 'main' in weather_data and 'weather' in weather_data:
            main_weather = weather_data['weather'][0]['main']
            description = weather_data['weather'][0]['description']

            temperature_kelvin = weather_data['main']['temp']
            feels_like_kelvin = weather_data['main']['feels_like']

            temperature_celsius = temperature_kelvin - 273.15
            feels_like_celsius = feels_like_kelvin - 273.15

            bot.reply_to(message, f'The weather in {city} is {main_weather} ({description}) Nya!\n'
                                  f'Temperature: {temperature_celsius:.2f}°C! :3\n'
                                  f'Feels like: {feels_like_celsius:.2f}°C! UwU')
        else:
            bot.reply_to(message, f'Sorry, I couldn\'t retrieve the weather information for {city}. Nya~ :(')
    except IndexError:
        bot.reply_to(message, 'Please provide a city name after the /weather command. UwU')
    except Exception as e:
        bot.reply_to(message, f'Something went wrong: {str(e)}. OwO')

if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)

