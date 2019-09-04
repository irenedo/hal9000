import requests
from yaml import safe_load

with open("config.yml", 'r') as stream:
    try:
        cfg = safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

config = cfg['modules']['weather']

def help()

def command(args):
    bot_return = {}
    if args == []:
      bot_return['error'] = True
      bot_return['message'] = "No parameters"
      bot_return['reactions'] = ["angry","eggplant"]
      bot_return['block'] = False
      return bot_return 
    else:
      weather = {}
      api_address = "https://api.openweathermap.org/data/2.5/weather?q={}" \
                    "&appid={}" \
                    "&units=metric".format(args[0], config['owappid'])
      json_data = requests.get(api_address).json()
      weather['current'] = json_data['main']['temp']
      weather['pressure'] = json_data['main']['pressure']
      weather['humidity'] = json_data['main']['humidity']
      weather['temp_max'] = json_data['main']['temp_max']
      weather['temp_min'] = json_data['main']['temp_min']
      bot_return['message'] = "Current temperature: *{}°C*\n" \
                              "Pressure: *{}Pa*\n" \
                              "Humidity: *{}%*\n" \
                              "Maximum temperature today: *{}°C*\n" \
                              "Minimum temperature today: *{}°C*".format(weather['current'],
                                                                         weather['pressure'],
                                                                         weather['humidity'],
                                                                         weather['temp_max'],
                                                                         weather['temp_min']),

      bot_return['block'] = False
      bot_return['error'] = False
      bot_return['reactions'] = []
      return bot_return


