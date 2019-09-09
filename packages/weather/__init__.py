"""
Weather module for hal9000
"""
import requests
from yaml import safe_load
from pycountry import countries

# Read the weather module's config from config.yml
try:
    with open("./config/config.yml", 'r') as stream:
        try:
            cfg = safe_load(stream)
        except YAMLError as err:
            print("config.yml is not a proper yaml file\n{}".format(err))
            sys.exit(2)
except Exception as err:
    print("Error openning the configuration file{}\n".format(err))
    sys.exit(2)

config = cfg['modules']['weather']


def response(error, reactions, block, message):
    """
    Build the message answer to the core
    :param error: True, False
    :param reactions: List of reactions to the original message
    :param block: Define if the message contains a slack block or a raw message (True/False)
    :param message: Message body. If the block parameter is True, it has to be a proper slack block
    :return: response
    """
    response = {}
    response['error'] = error
    response['reactions'] = reactions
    response['block'] = block
    response['message'] = message
    return response


def help():
    """
    In case the message is 'help', add the proper help answer from the base module
    :return: response
    """
    help_message = [
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': '*Usage:*'
            }
        },
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': '\tweather [current] [humidity] [pressure] [max] [min] city\n'
                        '\n*City format*:\n\t• City name\n\t• City name,country code'
            }
        },
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': '*Examples:*\n>weather Barcelona\n>weather Barcelona,es\n'
                        '>weather humidity Barcelona,es'
            }
        }    
    ]
    return response(False, [], True, help_message)
    

def command(args):
    """
    Processes the message
    :param args: Original message with words in a list
    :return: Return the proper message in a dictionary ->
            {
            'error' : [True/False],
            'reactions' [List of reactions to the message],
            'block': [The returned message is a slack block: True/False],
            'message': [Message body]
            }
    """
    if args == [] or 'help' in args:
        return help()
    else:
        stopwords = ['current', 'humidity', 'pressure', 'max', 'min']
        resultwords = [word for word in args if word.lower() not in stopwords]
        city = ' '.join(resultwords)
        api_address = 'https://api.openweathermap.org/data/2.5/weather?q={}' \
                      '&appid={}' \
                      '&units=metric'.format(city, config['owappid'])
        json_data = requests.get(api_address).json()
        if json_data.get('cod') is not 200:
            return response(True, ['worried'], False, '\n*{}*: {}'.format(city, json_data['message']))

        message = []

        alldata = True
        optionals = ['current', 'humidity', 'pressure', 'max', 'min']
        if any(word in args for word in optionals):
            alldata = False

        if ',' in city:
            city = city.split(',')[0]

        section = {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': '\nCity: *{}*\nCountry: *{}*\nMap: http://www.google.com/maps/place/{},{}'.format(
                            city.lower().title(),
                            countries.get(alpha_2=json_data['sys']['country']).name.lower().title(),
                            json_data['coord']['lat'],
                            json_data['coord']['lon'])
                    },
                    'accessory': {
                        'type': 'image',
                        'image_url': 'http://openweathermap.org/img/w/{}.png'.format(json_data['weather'][0]['icon']),
                        'alt_text': json_data['weather'][0]['description']
                    }
                } 
        message.append(section)
        section ={'type': 'divider'}
        message.append(section)
        if 'current' in args or alldata:
            section = {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': 'Current temperature: *{}°C*'.format(json_data['main']['temp'])
                        }
                    } 
            message.append(section)

        if 'humidity' in args or alldata:
            section = {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': 'Humidity: *{}%*'.format(json_data['main']['humidity'])
                        }
                    } 
            message.append(section)

        if 'pressure' in args or alldata:
            section = {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': 'Pressure: *{}Pa*'.format(json_data['main']['pressure'])
                        }
                    } 
            message.append(section)

        if 'max' in args or alldata:
            section = {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': 'Maximum temperature today: *{}°C*'.format(json_data['main']['temp_max'])
                        }
                    } 
            message.append(section)

        if 'min' in args or alldata:
            section = {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': 'Minimum temperature today: *{}°C*'.format(json_data['main']['temp_min'])
                        }
                    } 
            message.append(section)

        return response(False, ['thumbsup'], True, message)

