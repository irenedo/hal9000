
# HAL9000
Modular slack bot written en python. Originally intended to be used as a automated operator to manage the infrastructure from a single trusted point with custom cli python scripts to execute commands, ansible playblooks, kubectl and so on.

## Installation

### Slack
HAL9000 needs to use a slack app in your workspace with a bot user to exchange messages with it. This can be created from [https://api.slack.com/apps](https://api.slack.com/apps "https://api.slack.com/apps").

HAL9000 uses the Events API. To use it it's necessary to activate the Event Subscriptions in the app

![](https://raw.githubusercontent.com/irenedo/hal9000/master/images/event_subscriptions.png)

It needs to add the URL where the POST calls will be sent, and the subscription to **message.im** event name in the *Subscribe to Bot Events* section.
For development purposes, we will use [ngrok](https://ngrok.com/ "ngrok") to communicate slack with our developement environment. Please, read the [ngrok section](#ngrok) for this procedure.

From the **Basic Information** tab of the app, annotate the **signing secret**
From the **OAuth & Permissions** tab, annotate the **Bot User OAuth Access Token**

### Python script
The bot has been written in python 3 (has not been tested with python 2)
* Install the required modules
```bash
# pip3 install requirements.txt
```
* Configure the bot filling the file **config/config.yml**. You will the de slack API key and the signing secret provided by slack in the previous section.

* Start the script from the project's root directory. It will start a flask server to comunnicate with slack's events subscription API 
```bash
# python ./hal9000.py 
 * Serving Flask app "slackeventsapi.server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:3000/ (Press CTRL+C to quit)
```

### ngrok
For developmnet we can use ngrok to communicate with the events api with hal9000.  The download instructions can be found at [https://ngrok.com/download](https://ngrok.com/download "https://ngrok.com/download").

HAL9000 uses the port 3000 and ngrok must be started with the folowing command:
```bash
# ngrok http 3000
```
Annotate the https address

![](https://raw.githubusercontent.com/irenedo/hal9000/master/images/ngrok.png)

Add the https address followed by /slack/events in the Events Subscription URL of the slack app

![](https://raw.githubusercontent.com/irenedo/hal9000/master/images/ngrok_event_subscriptions.png)
## Adding custom modules
Custom modules are normal python modules inside _packages_ directory. To add your our modules you will have to create a new modules inside this directory.

### Mandatory functions
Some functions are mandatory:
* **init**: A init function to initialize the module. It will receive the module configuration from the config file
* **help**: A help message to send to slack in case the user asks for it. It has no parameters
* **command**: It will process the message written by the user. It receives the message from slack without the module name

### Returned message to slack
The message processed by **help** and **command** functions must be returned in a dictionary with the following key,values:

* **error**:  True/False. Warns slack that there was a problem processing the message
* **reactions**: List of emojis to send to the original message written by the user
* **message**: Message that the bot will write as answer to the command. It must be in a proper slack format and can be a message block, but in this case it has to be indicated wit the _block_ key
* **block**: True/False. The message returned is in block format

### Configuration
All the parameters needed by the module must be added to the _config.yml_ file, inside the _config_ directory. This is a _yaml_file with a _modules_section where your will have to add the module name (must be exactly the same name as the custom module) with your own configuration that will be passed to the **init** function at start. Example:
```yaml
---
config:
  slack_signing_secret: [Slack app signing secret]
  slack_api_key: [Slack's bot api key]
modules:
  weather:
    owappid: [openweather map api key]
  custom_module:
    param1: value1
    param2: value2
    ...
```
## Caveats
HAL9000 it's in a early development phase and a lot of errors and/or suggestions will be founded, I appreciate your collaboration
