import requests
import json

slack_icon_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuGqps7ZafuzUsViFGIremEL2a3NR0KO0s0RTCMXmzmREJd5m4MA&s'
slack_user_name = 'Johannes Roos'

def post_message_to_slack(channel, text, blocks = None, token=None):
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': token,
        'channel': "#" + channel,
        'text': text,
        'icon_url': slack_icon_url,
        'username': slack_user_name,
        'blocks': json.dumps(blocks) if blocks else None
    }).json()



def post_message_to_webhook(message):
    return requests.post('https://hooks.slack.com/services/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', {
        'text': message,
    }).json()