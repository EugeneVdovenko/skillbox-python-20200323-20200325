import time
from flask import Flask, request, abort

app = Flask(__name__)

messages = []

users = {
    'Nick': '12345'
}


@app.route("/")
def hello():
    return "Hello, world!"


@app.route('/status')
def status():
    return {
        'status': True,
        'name': 'Chatter',
        'time': time.strftime("%d-%m-%Y %H:%M:%S"),
        'messages': len(messages),
        'users': len(users)
    }


@app.route('/send', methods=['POST'])
def send():
    """
    JSON {
        username:
        password
    }
    :return: JSON {"ok": true}
    """
    username = request.json['username']
    password = request.json['password']

    if username in users:
        if password != users[username]:
            return abort(401)
    else:
        users[username] = password

    text = request.json['text']
    current_time = time.time()

    msg = {
        'username': username,
        'text': text,
        'time': current_time
    }
    messages.append(msg)

    print(messages)
    return {"ok": True}


@app.route('/history')
def history():
    after = float(request.args.get('after'))
    filtered = [message for message in messages if message['time'] > after]

    return {
        'messages': filtered
    }


app.run()
