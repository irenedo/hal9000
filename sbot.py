from slackeventsapi import SlackEventAdapter
from slack import WebClient
import bottasks
import reactions
import os

# Our app's Slack Event Adapter for receiving actions via the Events API
slack_events_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events")

# Create a SlackClient for your bot to use for Web API requests
client = WebClient(os.environ["SLACK_API_KEY"], timeout=30)

# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    # If the incoming message contains "hi", then respond with a "Hello" message
    if message.get("subtype") is not None:
        pass

    else:
        if "hi" in message.get('text').lower() or "hello" in message.get('text').lower():
            user = message['user']
            channel = message["channel"]
            reactions.write_message(message, client, "Hi <@{}>!".format(user),
                                    threaded=False,
                                    channel_id=channel)
        elif "cpu" in message.get('text').lower():
            channel = message['channel']
            cpu = bottasks.get_cpu()
            reactions.write_message(message, client, "CPU usage: *{}%*".format(cpu),
                                    threaded=False,
                                    channel_id=channel)

        elif "mem" in message.get('text').lower():
            channel = message['channel']
            mem = bottasks.get_mem()
            reactions.write_message(message, client, "Memory usage: *{}%*".format(mem),
                                    threaded=False,
                                    channel_id=channel)
        elif "weather" in message.get ('text').lower():
            channel = message['channel']
            city = message['text'].split(' ')[1]
            weather = bottasks.get_weather(city)
            reactions.write_message(message, client, "Current temperature: *{}°C*\n"
                                                     "Pressure: *{}Pa*\n"
                                                     "Humidity: *{}%*\n"
                                                     "Maximum temperature today: *{}°C*\n"
                                                     "Minimum temperature today: *{}°C*".format(weather['current'],
                                                                                                weather['pressure'],
                                                                                                weather['humidity'],
                                                                                                weather['temp_max'],
                                                                                                weather['temp_min']),
                                    threaded=False,
                                    channel_id=channel)
        else:
            channel = message['channel']
            reactions.write_message(message, client, "Sorry, I didn't understand you :thinking_face:",
                                    threaded=False,
                                    channel_id=channel)

# Example reaction emoji echo
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    event = event_data["event"]
    emoji = event["reaction"]
    channel = event["item"]["channel"]
    text = ":%s:" % emoji
    client.chat_postMessage(channel=channel, text=text)

# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(port=3000)

