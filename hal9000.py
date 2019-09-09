"""
HAL9000 core
"""

from slackeventsapi import SlackEventAdapter
from slack import WebClient
from yaml import safe_load, YAMLError
from json import dumps
import importlib
import sys

# import modules from the defined one in config.yml
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

# import base module
import base

# Our app's Slack Event Adapter for receiving actions via the Events API
slack_events_adapter = SlackEventAdapter(config['slack_signing_secret'], "/slack/events")

# Create a SlackClient for your bot to use for Web API requests
client = WebClient(config['slack_api_key'], timeout=30)


def call_module(modules, command, channel, thread_ts):
    """
    Call the correct module according to the message text
    :param modules: Modules dictionary
    :param command: Message received
    :param channel: Channel id
    :param thread_ts: Thread timestamp of the message
    """
    try:
        if command[0].lower() in modules.keys():
            ret = modules[command[0].lower()].command(command[1:])
        else:
            ret = base.command(command)
    except Exception as err:
        print("Error processing the message:{}\n{}".format(command,err))
    else:
        if ret['error']:
            client.chat_postMessage(
                channel=channel,
                text="I have a problem processing your request:\n{}".format(ret['message']),
            )
        else:
            if ret['block']:
                client.chat_postMessage(
                    channel=channel,
                    blocks=dumps(ret['message'])
                )                
            else:
                client.chat_postMessage(
                    channel=channel,
                    text=ret['message']
                ) 
        if ret['reactions'] is not []:
            for reaction in ret['reactions']:
                client.reactions_add(
                  channel=channel,
                  name=reaction,
                  timestamp=thread_ts
                )


@slack_events_adapter.on("message")
def handle_message(event_data):
    """
    Handles the received message from the Event API
    :param event_data: message data
    :return:
    """
    message = event_data["event"]
    # If the incoming message contains "hi", then respond with a "Hello" message
    if message.get("subtype") is not None and message.get('channel_type') is not 'im':
        pass
    else:
        command = message.get('text').split(" ")
        channel = message.get('channel')
        thread_ts = message.get('ts')
        call_module(pkg, command, channel, thread_ts)


# Error events
@slack_events_adapter.on("error")
def error_handler(message_error):
    """
    Handles errors with the API
    :param message_error: Message error
    """
    print("ERROR: " + str(message_error))


# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
try:
    slack_events_adapter.start(host='0.0.0.0', port=3000)
except Exception as err:
    print("Error starting the API server:\n{}".format(err))