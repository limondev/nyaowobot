
import telebot
from telebot.util import extract_arguments
from telebot.types import Message
import random
import requests
import schedule
import time
from config import TELEGRAM_API_TOKEN, api_key, pzpi_id
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)



@bot.message_handler(commands=['start', 'help'])
def send_kawaii_instructions(message):
    instructions = (
        "Konnichiwa~! To make your message kawaii, simply type /kawaii followed by your message. Also you can reply and quote this command.\n"
        "For example: /kawaii Hello, how are you? UwU\n"
        "Also, U can ask this bot for weather in your city, just type /weather followed by name of your city :3\n"
        "For example: /weather Kharkiv\n"
        "If you want to watch some anime, but don`t know which one exactly, you can use /randomanime OwO\n"
        "If your friend forgot to change keyboard layout and you don`t understand, what is he saying, you can always use /translate.\n"
        "Also you can reply and quote this command.\n"
        "If you wanna tell smth important to the chat, you can use /alert\n"
        "Author: @limoncello62"
    )
    bot.reply_to(message, instructions)


@bot.message_handler(commands=['kawaii'])
def kawaii_command(message: Message):
    user_message = extract_arguments(message.text)
    if user_message:
        answer = user_message
    elif message.reply_to_message:
        if message.quote and message.quote.text:
            answer = message.quote.text
        elif message.reply_to_message.text:
            answer = message.reply_to_message.text
        else:
            answer = "Nya~! The message that you replied to doesn't have any text."
    else:
        answer = "Nya~! Please provide a message after the /kawaii command."
    bot.reply_to(message, make_kawaii(answer))

def make_kawaii(user_message: str):
    emoticons = ["Nya!", "OwO", "UwU", ":3", "<3", ";3", ">_<", "><", "^-^", "^^", "ᵔᵕᵔ", "nyaaaa~", ">w<", ">∇<", '>:3', ">~<", '≽^•⩊•^≼', "≧◡≦"]
    random_emoticon = random.choice(emoticons)

    if random_emoticon in ["UwU", "OwO"]:
        for letter in ['s', 'l', 'r', 'x']:
            user_message = user_message.replace(letter, "w")

    return user_message + " " + random_emoticon


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
            rain_probability = weather_data.get('rain', {}).get('1h', 0)
            snow_probability = weather_data.get('snow', {}).get('1h', 0)

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
            elif "Mist" in main_weather:
                emoji = "🌫️"

            air_pollution_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={weather_data["coord"]["lat"]}&lon={weather_data["coord"]["lon"]}&appid={api_key}'
            air_pollution_response = requests.get(air_pollution_url)
            air_pollution_data = air_pollution_response.json()

            if 'list' in air_pollution_data and len(air_pollution_data['list']) > 0:
                air_quality = air_pollution_data['list'][0]['main']['aqi']
                bot.reply_to(message, f'The weather in {city} is {main_weather} {emoji} ({description}) Nya!\n'
                                      f'Temperature: {temperature_celsius:.2f}°C! :3\n'
                                      f'Feels like: {feels_like_celsius:.2f}°C! UwU\n'
                                      f'Wind Speed: {wind_speed} m/s! 🚩\n'
                                      f'Air Quality Index (AQI): {air_quality} OwO\n'
                                      f'Rain probability in next hour: {rain_probability*100:.0f}% 💦\n'
                                      f'Snow probability in next hour: {snow_probability*100:.0f}% ☃️')
            else:
                bot.reply_to(message, f'Sorry, I couldn\'t retrieve the air pollution information for {city}. Nya~ :(')
        else:
            bot.reply_to(message, f'Sorry, I couldn\'t retrieve the weather information for {city}. Nya~ :(')

    except IndexError:
        bot.reply_to(message, 'Please provide a city name after the /weather command. UwU')
    except Exception as e:
        bot.reply_to(message, f'Something went wrong: {str(e)}. OwO')


@bot.message_handler(commands=['randomanime'])
def get_random_anime(message):
    try:
        url = f'https://api.jikan.moe/v4/random/anime'
        response = requests.get(url)
        randani = response.json()
        bot.reply_to(message, f"Your random anime: {randani['data']['url']}")
    except Exception as e:
        bot.reply_to(message, f'Something went wrong: {str(e)}. OwO')


@bot.message_handler(commands=['translate'])
def trans(message):
    user_message = extract_arguments(message.text)
    answer = ''
    if user_message:
        answer = user_message
    elif message.reply_to_message:
        if message.quote and message.quote.text:
            answer = message.quote.text
        elif message.reply_to_message.text:
            answer = message.reply_to_message.text
    if answer:
        answer = map_en_to_ua(answer)
    else:
        answer = "Please provide a message to translate after the /translate command or reply to the message you want to translate. :3"
    bot.reply_to(message, answer)


# function for mapping (translating) from english keyboard layout to ukrainian
def map_en_to_ua(text):
    english_to_ukrainian = { "~": "₴", "!": "!", '@': '"', "#": "№", "$": ";", "%": "%", "^": ":", "&": "?", "*": "*", "(": "(",")": ")", "_": "_", "+": "+",
                             "Q": "Й", "W": "Ц", "E": "У", "R": "К", "T": "Е", "Y": "Н", "U": "Г", "I": "Ш", "O": "Щ", "P": "З", "{": "Х", "}": "Ї",
                             "A": "Ф", "S": "І", "D": "В", "F": "А", "G": "П", "H": "Р", "J": "О", "K": "Л", "L": "Д", ":": "Ж", '"': 'Є', "|": "/",
                             "Z": "Я", "X": "Ч", "C": "С", "V": "М", "B": "И", "N": "Т", "M": "Ь", "<": "Б", ">": "Ю", "?": ",",
                             "`": "'", "1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "0": "0", "-": "-", "=": "=",
                             "q": "й", "w": "ц", "e": "у", "r": "к", "t": "е", "y": "н", "u": "г", "i": "ш", "o": "щ", "p": "з", "[": "х", "]": "ї",
                             "a": "ф", "s": "і", "d": "в", "f": "а", "g": "п", "h": "р", "j": "о", "k": "л", "l": "д", ";": "ж", "'": "є", "\\": "\\",
                             "z": "я", "x": "ч", "c": "с", "v": "м", "b": "и", "n": "т", "m": "ь", ",": "б", ".": "ю", "/": "." }
    # subfunction for mapping characters
    def map_character(char):
        return english_to_ukrainian.get(char, char)

    mapped = "".join(map_character(letter) for letter in text)
    return mapped


@bot.message_handler(commands=['alert', 'ALERT'])
def kok(message):
    user_message = extract_arguments(message.text)
    if user_message:
        answer = user_message
    elif message.reply_to_message:
        if message.quote and message.quote.text:
            answer = message.quote.text
        elif message.reply_to_message.text:
            answer = message.reply_to_message.text
        else:
            answer = "THERE IS NO TEXT"
    else:
        answer = ''
    symbols_amount = random.randint(5, 50)
    answer += create_random_alert_symbols(symbols_amount)
    bot.reply_to(message, answer.upper())


def create_random_alert_symbols(amount:int) -> str:
    alert_symbols = ["❗️", "🔉", "🆘", "🗣", "⚠️", "🔥"]
    return "".join(random.choice(alert_symbols) for i in range(amount))


# from this part there are some silly commands for my friends
@bot.message_handler(commands=['masshironayuki'])
def song(message):
    bot.reply_to(message, "https://www.youtube.com/watch?v=vKhpQTYOpUU")

@bot.message_handler(commands=['serhii'])
def maps(message):
    random_num = random.randint(1, 100)
    bot.reply_to(message, f"МАПИ " * random_num)

@bot.message_handler(commands=['mykyta'])
def ro(message):
    random_num = random.randint(1, 100)
    bot.reply_to(message, "Родичі " * random_num + "\nAnd complaining about стипендія, of course")

@bot.message_handler(commands=['dimasik'])
def ro(message):
    random_num = random.randint(1, 100)
    bot.reply_to(message, f"ПИВО " * random_num)

@bot.message_handler(commands=['liliia'])
def ipso(message):
    messages = ["київстар лежить бо це теж один із планів цифрової трансформації?", "Київ візьмуть за 3 дні", "А хто піде відвойовувати його? У нас тупо нема кому", "Ну завтра ядеркою вʼїбати по Києву можуть", "збивають тільки в києві, інші міста хай хавають", "Ось би як в Росії, у яких склади в Сибірі, їм там все за 10-14 днів з Китаю приходить", "цікаво скіки людей лишиться в україні коли відкриють кордони", "живемо на рівні розвитку уганди якоїсь", "да їм тут 30 км пройти і вони Харків захоплять"]
    bot.reply_to(message, f"{random.choice(messages)}")

@bot.message_handler(commands=['sarcasm'])
def ro(message):
    bot.reply_to(message, "(САРКАЗМ!!!!!!!!!)")

@bot.message_handler(commands=['ilya'])
def ro(message):
    bot.reply_to(message, "C# (произносится си шарп) — объектно-ориентированный язык программирования общего назначения. Разработан в 1998—2001 годах группой инженеров компании Microsoft под руководством Андерса Хейлсберга и Скотта Вильтаумота как язык разработки приложений для платформы Microsoft .NET Framework и .NET Core. Впоследствии был стандартизирован как ECMA-334 и ISO/IEC 23270. C# относится к семье языков с C-подобным синтаксисом, из них его синтаксис наиболее близок к C++ и Java. Язык имеет статическую типизацию, поддерживает полиморфизм, перегрузку операторов (в том числе операторов явного и неявного приведения типа), делегаты, атрибуты, события, переменные, свойства, обобщённые типы и методы, итераторы, анонимные функции с поддержкой замыканий, LINQ, исключения, комментарии в формате XML. Переняв многое от своих предшественников — языков C++, Delphi, Модула, Smalltalk и, в особенности, Java — С#, опираясь на практику их использования, исключает некоторые модели, зарекомендовавшие себя как проблематичные при разработке программных систем, например, C# в отличие от C++ не поддерживает множественное наследование классов (между тем допускается множественная реализация интерфейсов).")

@bot.message_handler(commands=['rostik'])
def ipso(message):
    messages = ["КАКИМ будет НОВОЕ КОНТРНАСТУПЛЕНИЕ Украины? ПОДРОБНО о ПЛАНАХ ВСУ на 2024 год","ВОТ ТАК ОРУЖИЕ! ВСУ начали подготовку К ...", "ДОН-ДОН ИГРАЕТ с Кремлем? РАЗБОР ТУПЫХ заявлений КАДЫРОВА", "Путину стоит ОПАСАТЬСЯ ЭТОГО ⚡️ После ВЫБОРОВ 2024 на Россию ОБРУШИТСЯ...", "ТОП-5 ХИТОВ российской ПРОПАГАНДЫ: какой БРЕД несли РТЫ ПУТИНА в 2023", "Дагестанские ученые разработали очко барану"]
    bot.reply_to(message, f"{random.choice(messages)}")

def tagi(user_ids):
    tags = ''
    for user_id in user_ids:
        tags += f'{user_id}\n'
    return tags

def split_tags(user_ids, chunk_size):
    for i in range(0, len(user_ids), chunk_size):
        yield user_ids[i:i + chunk_size]

@bot.message_handler(commands=['tag'])
def xoxly(message):
    tagged_users_chunks = list(split_tags(pzpi_id, 5))
    for chunk in tagged_users_chunks:
        bot.reply_to(message, f"Хохли, загальний збір!\n{tagi(chunk)}")

@bot.message_handler(commands=["randomshurup"])
def shurup(message: Message):
    shurup_data = ["Шуруп з потайною головкою для твердих порід деревини TORX", "Шуруп гіпсокартонний по дереву", "Шуруп з потайною головкою з хрестоподібним шліцом", "Шуруп для гіпсокартону до дерева на стрічці оцинкований ESSVE", "Шуруп з потайною головкою для твердих порід деревини POZIDRIV (PZ)", "Шуруп з напівкруглою головкою з хрестоподібним шліцом (нержавійна сталь А2)", "Шуруп для твердого гіпсокартону на стрічці ESSVE фосфат", "Комбінований гвинт-шуруп", "Шуруп - конфірмат", "Комбінований шуруп-шуруп", "Шуруп гіпсокартонний самосверлящий", "Шуруп для зшивання гіпсокартону оцинкований", "Шуруп для легкого бетону півкруг / WAF"]
    shurup_links = ["https://fixpro.ua/image/cache/catalog/photo5195223043339826598-1000x1000.jpg", "https://fixpro.ua/image/cache/catalog/photo5390828558512927507-1000x1000.jpg", "https://fixpro.ua/image/cache/catalog/photo5406747236320261296-1000x1000.jpg", "https://fixpro.ua/image/cache/catalog/%D1%84%D0%BE%D1%82%D0%BA%D0%B8/%D0%A8%D1%83%D1%80%D1%83%D0%BF%D1%8B-%D1%81%D0%B0%D0%BC%D0%BE%D1%80%D0%B5%D0%B7%D1%8B/%D0%A7%D0%B5%D1%80%D0%BD%D1%8B%D0%B5%20%D0%B8%20%D0%91%D0%BB%D0%BE%D1%85%D0%B0/735171-1000x1000.png", "https://fixpro.ua/image/cache/catalog/%D1%84%D0%BE%D1%82%D0%BA%D0%B8/%D0%A8%D1%83%D1%80%D1%83%D0%BF%D1%8B-%D1%81%D0%B0%D0%BC%D0%BE%D1%80%D0%B5%D0%B7%D1%8B/%D0%A1%D0%B0%D0%BC%D0%BE%D1%80%D0%B5%D0%B7%D1%8B%20%D0%96%D0%B5%D0%BB,%D0%91%D0%B5%D0%BB,A2,%20%D0%A1%D1%84%D0%B5%D1%80%D0%B0%20%D0%94%D0%B5%D1%80+%D0%9C%D0%B5%D1%82/fixpro-samorez-dlya-tverdih-porod-1000x1000.jpg", "https://fixpro.ua/image/cache/catalog/333/fixpro_shurup_z_napivkug_golov_a2-1000x1000.jpg", "https://fixpro.ua/image/cache/catalog/photo_l/fix_pro_samorez_na_lente_phosphat-1000x1000.jpg", "https://fixpro.ua/image/cache/catalog/176-1000x1000.png", "https://fixpro.ua/image/cache/catalog/%20%D0%B4%D0%BB%D1%8F%20%D1%85%D0%B8%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85%20%D0%B0%D0%BD%D0%BA%D0%B5%D1%80%D0%BE%D0%B2/2819708119_w640_h640_shurup-konfirmat-5-x-1000x1000.jpg", "https://fixpro.ua/image/cache/catalog/shurup-20-1000x1000.jpg", "https://fixpro.ua/image/cache/catalog/%D1%84%D0%BE%D1%82%D0%BA%D0%B8/%D0%A8%D1%83%D1%80%D1%83%D0%BF%D1%8B-%D1%81%D0%B0%D0%BC%D0%BE%D1%80%D0%B5%D0%B7%D1%8B/%D0%A7%D0%B5%D1%80%D0%BD%D1%8B%D0%B5%20%D0%B8%20%D0%91%D0%BB%D0%BE%D1%85%D0%B0/fixpro-samorez_s-burom-1000x1000.jpg", "https://fixpro.ua/image/cache/catalog/photo_l/fixpro-samorez-essve-1000x1000.JPG", "https://fixpro.ua/image/cache/catalog/333/fixpro_waf_dlya_leg_beton-1000x1000.jpg"]
    shurup_dict = {shurup_data[i]: shurup_links[i] for i in range(min(len(shurup_data), len(shurup_links)))}
    random_key = random.choice(list(shurup_dict.keys()))
    bot.reply_to(message, f"[{random_key}]({shurup_dict[random_key]})", parse_mode='Markdown')

def send_random_screw():
    shurup_data = ["Шуруп з потайною головкою для твердих порід деревини TORX", "Шуруп гіпсокартонний по дереву", "Шуруп з потайною головкою з хрестоподібним шліцом", "Шуруп для гіпсокартону до дерева на стрічці оцинкований ESSVE", "Шуруп з потайною головкою для твердих порід деревини POZIDRIV (PZ)", "Шуруп з напівкруглою головкою з хрестоподібним шліцом (нержавійна сталь А2)", "Шуруп для твердого гіпсокартону на стрічці ESSVE фосфат", "Комбінований гвинт-шуруп", "Шуруп - конфірмат", "Комбінований шуруп-шуруп", "Шуруп гіпсокартонний самосверлящий", "Шуруп для зшивання гіпсокартону оцинкований", "Шуруп для легкого бетону півкруг / WAF"]
    shurup_links = ["https://fixpro.ua/image/cache/catalog/photo5195223043339826598-1000x1000.jpg", "https://fixpro.ua/image/cache/catalog/photo5390828558512927507-1000x1000.jpg", "https://fixpro.ua/image/cache/catalog/photo5406747236320261296-1000x1000.jpg", "https://fixpro.ua/image/cache/catalog/%D1%84%D0%BE%D1%82%D0%BA%D0%B8/%D0%A8%D1%83%D1%80%D1%83%D0%BF%D1%8B-%D1%81%D0%B0%D0%BC%D0%BE%D1%80%D0%B5%D0%B7%D1%8B/%D0%A7%D0%B5%D1%80%D0%BD%D1%8B%D0%B5%20%D0%B8%20%D0%91%D0%BB%D0%BE%D1%85%D0%B0/735171-1000x1000.png", "https://fixpro.ua/image/cache/catalog/%D1%84%D0%BE%D1%82%D0%BA%D0%B8/%D0%A8%D1%83%D1%80%D1%83%D0%BF%D1%8B-%D1%81%D0%B0%D0%BC%D0%BE%D1%80%D0%B5%D0%B7%D1%8B/%D0%A1%D0%B0%D0%BC%D0%BE%D1%80%D0%B5%D0%B7%D1%8B%20%D0%96%D0%B5%D0%BB,%D0%91%D0%B5%D0%BB,A2,%20%D0%A1%D1%84%D0%B5%D1%80%D0%B0%20%D0%94%D0%B5%D1%80+%D0%9C%D0%B5%D1%82/fixpro-samorez-dlya-tverdih-porod-1000x1000.jpg", "https://fixpro.ua/image/cache/catalog/333/fixpro_shurup_z_napivkug_golov_a2-1000x1000.jpg", "https://fixpro.ua/image/cache/catalog/photo_l/fix_pro_samorez_na_lente_phosphat-1000x1000.jpg", "https://fixpro.ua/image/cache/catalog/176-1000x1000.png", "https://fixpro.ua/image/cache/catalog/%20%D0%B4%D0%BB%D1%8F%20%D1%85%D0%B8%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85%20%D0%B0%D0%BD%D0%BA%D0%B5%D1%80%D0%BE%D0%B2/2819708119_w640_h640_shurup-konfirmat-5-x-1000x1000.jpg", "https://fixpro.ua/image/cache/catalog/shurup-20-1000x1000.jpg", "https://fixpro.ua/image/cache/catalog/%D1%84%D0%BE%D1%82%D0%BA%D0%B8/%D0%A8%D1%83%D1%80%D1%83%D0%BF%D1%8B-%D1%81%D0%B0%D0%BC%D0%BE%D1%80%D0%B5%D0%B7%D1%8B/%D0%A7%D0%B5%D1%80%D0%BD%D1%8B%D0%B5%20%D0%B8%20%D0%91%D0%BB%D0%BE%D1%85%D0%B0/fixpro-samorez_s-burom-1000x1000.jpg", "https://fixpro.ua/image/cache/catalog/photo_l/fixpro-samorez-essve-1000x1000.JPG", "https://fixpro.ua/image/cache/catalog/333/fixpro_waf_dlya_leg_beton-1000x1000.jpg"]
    shurup_dict = {shurup_data[i]: shurup_links[i] for i in range(min(len(shurup_data), len(shurup_links)))}
    random_key = random.choice(list(shurup_dict.keys()))
    message = f"Шуруп дня: [{random_key}]({shurup_dict[random_key]})"
    bot.send_message(chat_id='-1001908899737', text=message, parse_mode='Markdown')



if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
    while True:
        schedule.every().day.at("12:46").do(send_random_screw)
        schedule.run_pending()
        time.sleep(1)