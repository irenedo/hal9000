import requests
from yaml import safe_load
from sys import argv

try:
    with open("config.yml", 'r') as stream:
        try:
            cfg = safe_load(stream)
        except YAMLError as err:
            print("config.yml is not a proper yaml file\n{}".format(err))
            sys.exit(2)
except Exception as err:
    print("Error openning the configuration file{}\n".format(err))
    sys.exit(2)

config = cfg['modules']['weather']

def help():
    bot_return = {}
    bot_return['error'] = False
    bot_return['reactions'] = []
    bot_return['block'] = True
    bot_return['message'] = [
        {
            'type' : 'section' ,
            'text' : {
                'type' : 'mrkdwn' ,
                'text' : '*Usage:*' 
            }
        },
        {
            'type' : 'section' ,
            'text' : {
                'type' : 'mrkdwn' ,
                'text' : '\tweather [current] [humidity] [pressure] [max] [min] city\n\n*City format*:\n\t• City name\n\t• City name,country code' 
            }
        },
        {
            'type' : 'section' ,
            'text' : {
                'type' : 'mrkdwn' ,
                'text' : '*Examples:*\n>weather Barcelona\n>weather Barcelona,es\n>weather humidity Barcelona,es' 
            }
        }    
    ]
    return bot_return
    

def command(args):
    bot_return = {}
    if args == [] or 'help' in args:
        return help()
    else:
        weather = {}
        city = args[-1]
        api_address = 'https://api.openweathermap.org/data/2.5/weather?q={}' \
                    '&appid={}' \
                    '&units=metric'.format(city, config['owappid'])
        json_data = requests.get(api_address).json()

        if json_data.get('cod') is not 200:
            bot_return['error'] = True
            bot_return['message'] = '\n*{}*: {}'.format(city, json_data['message']) 
            bot_return['reactions'] = ['worried']
            bot_return['block'] = False
            return bot_return            

        bot_return['message'] = []

        alldata = True
        optionals = ['current', 'humidity', 'pressure', 'max', 'min']
        if any(word in args for word in optionals):
            alldata = False

        if 'current' in args or alldata:
            section = {
                        'type' : 'section' ,
                        'text' : {
                            'type' : 'mrkdwn' ,
                            'text' : 'Current temperature: *{}°C*'.format(json_data['main']['temp']) 
                        }
                    } 
            bot_return['message'].append(section)

        if 'humidity' in args or alldata:
            section = {
                        'type' : 'section' ,
                        'text' : {
                            'type' : 'mrkdwn' ,
                            'text' : 'Humidity: *{}%*'.format(json_data['main']['humidity']) 
                        }
                    } 
            bot_return['message'].append(section)

        if 'pressure' in args or alldata:
            section = {
                        'type' : 'section' ,
                        'text' : {
                            'type' : 'mrkdwn' ,
                            'text' : 'Pressure: *{}Pa*'.format(json_data['main']['pressure']) 
                        }
                    } 
            bot_return['message'].append(section)


        if 'max' in args or alldata:
            section = {
                        'type' : 'section' ,
                        'text' : {
                            'type' : 'mrkdwn' ,
                            'text' : 'Maximum temperature today: *{}°C*'.format(json_data['main']['temp_max']) 
                        }
                    } 
            bot_return['message'].append(section)

        if 'min' in args or alldata:
            section = {
                        'type' : 'section' ,
                        'text' : {
                            'type' : 'mrkdwn' ,
                            'text' : 'Minimum temperature today: *{}°C*'.format(json_data['main']['temp_min']) 
                        }
                    } 
            bot_return['message'].append(section)


        bot_return['block'] = True
        bot_return['error'] = False
        bot_return['reactions'] = ['thumbsup']
        return bot_return


if __name__ == '__main__':
    print(command(argv[1:]))