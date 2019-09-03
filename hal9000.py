from slackeventsapi import SlackEventAdapter
from slack import WebClient
from yaml import safe_load
import importlib
import sys


with open("config.yml", 'r') as stream:
    try:
        cfg = safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

config = cfg['config']
sys.path.append('./packages')
pkg = {mod:importlib.import_module(mod) for mod in cfg['modules'].keys()}

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
            ret = pkg[command].command(client,message.get('text').split(" ")[1:])
            if ret['block']:
                client.chat_postMessage(
                    channel=channel,
                    block=ret['message'][0],
                    thread_ts=thread_ts
                )                
            else:
                client.chat_postMessage(
                    channel=channel,
                    text=ret['message'][0],
                    thread_ts=thread_ts
                ) 
        else:
            thread_ts = message.get('ts')
            channel = message.get('channel')
            client.chat_postMessage(
                channel=channel,
                text="Sorry, I didn't understand you :thinking_face:",
                thread_ts=thread_ts
            )

# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(host='0.0.0.0', port=3000)