import os
import time
from slackclient import SlackClient
import enchant
# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")
d = enchant.Dict("en")

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def handle_command(command, channel):
    if not (command.startswith("Suggeste")):
        response = "Suggested: "
        tmp = d.suggest(str(command))
        for i in tmp:
            response += i+" , "
        slack_client.api_call("chat.postMessage", channel=channel,text=response[:-3],as_user=True)

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                return output['text'], output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")