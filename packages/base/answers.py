from random import randint
answers = {
			'regards': 
				["hi", "hello", "hey", "helloo", "hellooo", "g morining", "gmorning", "good morning", "morning", "good day",
		        "good afternoon", "good evening", "greetings", "greeting", "good to see you", "its good seeing you",
		        "how are you", "how're you", "how are you doing", "how ya doin'", "how ya doin", "how is everything",
		        "how is everything going", "how's everything going", "how is you", "how's you", "how are things", "how're things",
		        "how is it going", "how's it going", "how's it goin'", "how's it goin", "how is life been treating you",
		        "how's life been treating you", "how have you been", "how've you been", "what is up", "what's up", "what is cracking",
		         "what's cracking", "what is good", "what's good", "what is happening", "what's happening", "what is new", "what's new"],
            'unknown':
            	["Sorry, I didn't understand you", "what?", "Please, repeat it again", "What did you say?", "I don't catch you"]
            }

def answer(action):
	return answers[action][randint(0,len(answers[action])-1)]
