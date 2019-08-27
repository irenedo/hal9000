import psutil
import requests


def get_cpu():
    return psutil.cpu_percent()


def get_mem():
    return dict(psutil.virtual_memory()._asdict())['percent']


def get_weather(city):
    weather = {}
    api_address = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=603ff328fea64060f7ae52f777594618&units=metric".format(city)
    json_data = requests.get(api_address).json()
    weather['current'] = json_data['main']['temp']
    weather['pressure'] = json_data['main']['pressure']
    weather['humidity'] = json_data['main']['humidity']
    weather['temp_max'] = json_data['main']['temp_max']
    weather['temp_min'] = json_data['main']['temp_min']
    return weather
