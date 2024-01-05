import telebot
import random
import requests

from config import TELEGRAM_API_TOKEN, api_key
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_kawaii_instructions(message):
    instructions = (
        "Konnichiwa~! To make your message kawaii, simply type /kawaii followed by your message.\n"
        "For example: /kawaii Hello, how are you? UwU\n"
        "Also, U can ask this bot for weather in your city, just type /weather followed by mane of your city :3\n"
        "For example: /weather Kharkiv\n"
        "If you want to watch some anime, but don`t know which one exactly, you can use /randomanime OwO"
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
    string_list = ["Nya!", "OwO", "UwU", ":3", "<3", ";3", ">_<", "><", "^-^", "^^", "ᵔᵕᵔ", "nyaaaa~"]
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
            wind_speed = weather_data['wind']['speed']
            temperature_kelvin = weather_data['main']['temp']
            feels_like_kelvin = weather_data['main']['feels_like']

            temperature_celsius = temperature_kelvin - 273.15
            feels_like_celsius = feels_like_kelvin - 273.15
            emoji = ''
            if "Clear" in main_weather:
                emoji = "☀️"
            elif "Clouds" in main_weather:
                emoji = "☁️"
            elif "Rain" in main_weather:
                emoji = "🌧️"
            elif "Snow" in main_weather:
                emoji = "❄️"

            air_pollution_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={weather_data["coord"]["lat"]}&lon={weather_data["coord"]["lon"]}&appid={api_key}'
            air_pollution_response = requests.get(air_pollution_url)
            air_pollution_data = air_pollution_response.json()

            if 'list' in air_pollution_data and len(air_pollution_data['list']) > 0:
                air_quality = air_pollution_data['list'][0]['main']['aqi']
                bot.reply_to(message, f'The weather in {city} is {main_weather} {emoji} ({description}) Nya!\n'
                                      f'Temperature: {temperature_celsius:.2f}°C! :3\n'
                                      f'Feels like: {feels_like_celsius:.2f}°C! UwU\n'
                                      f'Wind Speed: {wind_speed} m/s! 🌬️\n'
                                      f'Air Quality Index (AQI): {air_quality} OwO')
            else:
                bot.reply_to(message, f'Sorry, I couldn\'t retrieve the air pollution information for {city}. Nya~ :(')
        else:
            bot.reply_to(message, f'Sorry, I couldn\'t retrieve the weather information for {city}. Nya~ :(')
    except IndexError:
        bot.reply_to(message, 'Please provide a city name after the /weather command. UwU')
    except Exception as e:
        bot.reply_to(message, f'Something went wrong: {str(e)}. OwO')


@bot.message_handler(commands=['randomanime'])
def random_anime_generator(message):
    try:
        url = f'https://api.jikan.moe/v4/random/anime'
        response = requests.get(url)
        randani = response.json()
        bot.reply_to(message, f"Your random anime: {randani['data']['url']}")
    except Exception as e:
        bot.reply_to(message, f'Something went wrong: {str(e)}. OwO')

if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)



