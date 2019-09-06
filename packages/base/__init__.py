from random import randint

greetings = ["hi", "hello", "hey", "helloo", "hellooo", "g morining", "gmorning", "good morning", "morning", "good day",
            "good afternoon", "good evening", "greetings", "greeting", "good to see you", "its good seeing you",
            "how are you", "how're you", "how are you doing", "how ya doin'", "how ya doin", "how is everything",
            "how is everything going", "how's everything going", "how is you", "how's you", "how are things", "how're things",
            "how is it going", "how's it going", "how's it goin'", "how's it goin", "how is life been treating you",
            "how's life been treating you", "how have you been", "how've you been", "what is up", "what's up", "what is cracking",
             "what's cracking", "what is good", "what's good", "what is happening", "what's happening", "what is new", "what's new"]

def response(error, reactions, block, message):
    response = {}
    response['error'] = error
    response['reactions'] = reactions
    response['block'] = block
    response['message'] = message
    return response


def help():
    help_message = "This is the base help message"
    return response(False, [], False, help_message)
    

def command(args):

    if 'help' in args:
        return help()
    elif args[0].lower() in ['hello', 'hi', 'hey', 'good morning', 'good day', 'wassup']:
        return response(False, ['smiley'], False, greetings[randint(0,len(greetings)-1)])
    else:
        return response(False, ['cry'], False, "Sorry, I didn't understand you")
