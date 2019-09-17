"""
HAL9000 core
"""
from json import dumps
import halinit
import packages.base


pkg, config = halinit.init_modules()
slack_events_adapter = halinit.init_adapter(config['slack_signing_secret'], "/slack/events")
client = halinit.init_client(config['slack_api_key'])

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
            ret = packages.base.command(command)
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


halinit.start_hal9000(slack_events_adapter)