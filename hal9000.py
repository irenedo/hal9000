from slackeventsapi import SlackEventAdapter
from slack import WebClient
from yaml import safe_load, YAMLError
import importlib
import sys

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

config = cfg['config']
sys.path.append('./packages')

try:
    pkg = {mod:importlib.import_module(mod) for mod in cfg['modules'].keys()}
except Exception as err:
    print("Error importing modules:\n{}".format(err))
    sys.exit(2)

# Our app's Slack Event Adapter for receiving actions via the Events API
slack_events_adapter = SlackEventAdapter(config['slack_signing_secret'], "/slack/events")

# Create a SlackClient for your bot to use for Web API requests
client = WebClient(config['slack_api_key'], timeout=30)


# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    # If the incoming message contains "hi", then respond with a "Hello" message
    if message.get("subtype") is not None and message.get('channel_type') is not 'im':
        pass
    else:
        command = message.get('text').split(" ")[0].lower()
        if command in pkg.keys():
            user = message['user']
            channel = message["channel"]
            thread_ts = message.get('ts')
            try:
                ret = pkg[command].command(message.get('text').split(" ")[1:])
            except Exception as err:
                print("Problem calling the module {}\n{}".format(command,err))
            else:
                if ret['error']:
                    mes = client.chat_postMessage(
                        channel=channel,
                        text="Error executing command: *{}*".format(ret['message']),
                    )
                else:
                    if ret['block']:
                        mes = client.chat_postMessage(
                            channel=channel,
                            block=ret['message'][0],
                            thread_ts=thread_ts
                        )                
                    else:
                        mes = client.chat_postMessage(
                            channel=channel,
                            text=ret['message'][0],
                            thread_ts=thread_ts
                        ) 
                if ret['reactions'] is not []:
                    for reaction in ret['reactions']:
                        client.reactions_add(
                          channel=channel,
                          name=reaction,
                          timestamp=mes['message']['ts']
                        )
        else:
            channel = message.get('channel')
            client.chat_postMessage(
                channel=channel,
                text="Sorry, I didn't understand you :thinking_face:"
            )

# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
try:
    slack_events_adapter.start(host='0.0.0.0', port=3000)
except Exception as err:
    print("Error starting the API server:\n{}".format(err))