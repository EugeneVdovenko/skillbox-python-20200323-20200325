import requests
import time
from datetime import datetime

after = 0


def get_message(after):
    response = requests.get(
        'http://127.0.0.1:5000/history',
        params={'after': after})
    data = response.json()
    return data['messages']


def print_message(message):
    text = message['text']
    nick = message['username']
    timestamp = float(message['time'])

    ct = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

    print(ct, nick)
    print(text)
    print()


while True:
    messages = get_message(after)
    if messages:
        after = messages[-1]['time']

        for message in messages:
            print_message(message)
            if message['time'] > after:
                after = message['time']
    time.sleep(1)
