"""
Init HAL9000 modules and all the connections 
"""
from slackeventsapi import SlackEventAdapter
from slack import WebClient
from yaml import safe_load, YAMLError
import importlib
import sys

def init_modules():
    """
    Import all the modules defined in the config.yml file
    :return:
        pkg: dictionary with the name of the module as a key and a pointer to the module as a value
        config: Config file as a dictionary
    """
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

    config = cfg['config']

    sys.path.append('./packages')
    try:
        pkg = {mod: importlib.import_module(mod) for mod in cfg['modules'].keys()}
    except Exception as err:
        print("Error importing modules:\n{}".format(err))
        sys.exit(2)

    # Initialize all modules calling their init function
    for module in pkg.keys():
        pkg[module].init(cfg['modules'][module])

    return pkg, config


def init_adapter(signing_secret, uri):
    """
    Init the Slack Event Adapter for receiving actions via the Events API
    :param signing_secret: App's signing secret to validate the connection
    :param uri: uri where the adapter will be listening
    :return: slack event adapter object
    """
    return SlackEventAdapter(signing_secret, uri)

def init_client(api_key):
    """
    Create a SlackClient for the bot to use for Web API requests
    :param api_key: API key to validate the API calls
    :return: webclient object
    """
    return WebClient(api_key, timeout=30)

def start_hal9000(events_adapter):
    """
    Once we have our event listeners configured, we can start the
    Flask server with the uri defined in the init_adapter function
    """
    try:
        events_adapter.start(host='0.0.0.0', port=3000)
    except Exception as err:
        print("Error starting the API server:\n{}".format(err))