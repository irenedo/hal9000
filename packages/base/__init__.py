"""
Manages all the messages that doesn't belong to any defined custom modules
"""
import packages.base.answers


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
    help_message = "This is the base help message"
    return response(False, [], False, help_message)
    

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
    if 'help' in args:
        return help()
    elif args[0].lower() in ['hello', 'hi', 'hey', 'good morning', 'good day', 'wassup']:
        return response(False, ['smiley'], False, answers.answer('regards'))
    else:
        return response(False, ['cry'], False, answers.answer('unknown'))
