import requests

# api_key = '260734bea560cd99def075c4397fb858'
# url = f'http://api.openweathermap.org/data/2.5/weather?q=kharkiv&appid={api_key}'
response = requests.get("https://wttr.in/kharkiv")
weather_data = response.json()
print(weather_data)
