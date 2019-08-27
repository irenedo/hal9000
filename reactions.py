

def write_message(data, client, message, threaded, channel_id):
    if threaded:
        thread_ts = data['ts']
        client.chat_postMessage(
            channel=channel_id,
            text=message,
            thread_ts=thread_ts
        )
    else:
        client.chat_postMessage(
            channel=channel_id,
            text=message
        )


def write_block(data, webclient, block, threaded, channel_id):
    if threaded:
        thread_ts = data['ts']
        webclient.chat_postMessage(
            channel=channel_id,
            blocks=block,
            thread_ts=thread_ts
        )
    else:
        webclient.chat_postMessage(
            channel=channel_id,
            blocks=block
        )
