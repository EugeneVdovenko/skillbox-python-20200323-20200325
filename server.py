import time
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, world!"


@app.route('/status')
def status():
    return {
        'status': True,
        'name': 'Chatter',
        'time': time.strftime("%d-%m-%Y %H:%M:%S")
    }


@app.route('/send')
def send():
    pass


@app.route('/routes')
def routes():
    pass

app.run()
