from flask import Flask, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import time

cur_dir = os.path.abspath(os.path.dirname(__file__))
version = '0.0.1a'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(cur_dir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), index=True)
    time = db.Column(db.String(100))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(30), index=True, unique=True)
    password = db.Column(db.String(30))
    messages = db.relationship('Message', backref='author', lazy='dynamic')


@app.route("/")
def hello():
    info = status()
    return render_template("index.html", info=info)


@app.route('/status')
def status():
    """
    Получаем информацию по сервису
    :return: JSON
    """
    return {
        'status': True,
        'name': 'Chatter',
        'time': time.strftime("%d-%m-%Y %H:%M:%S"),
        'messages': Message.query.count(),
        'users': User.query.count(),
        'version': version
    }


@app.route('/send', methods=['POST'])
def send():
    """
    Принимаем JSON
    {
        "username": str,
        "password": str,
        "text": str
    }
    и записывает в базу данных
    :return: JSON {"ok": true}
    """
    username = request.json['username']
    password = request.json['password']

    cur_user = User.query.filter_by(user=username).first()
    if cur_user:
        if cur_user.password != password:
            return abort(401)
    else:
        cur_user = User(user=username, password=password)
        db.session.add(cur_user)
        db.session.commit()

    text = request.json['text']
    current_time = time.time()

    message = Message(message=text, time=current_time, user=cur_user.id)
    db.session.add(message)
    db.session.commit()

    return {"ok": True}


@app.route('/history')
def history():
    """
    История сообщений
    :return: JSON
    """
    after = float(request.args.get('after'))
    messages = Message.query.filter(Message.time > after).all()
    filtred = []
    for message in messages:
        filtred.append({
            'text': message.message,
            'username': message.author.user,
            'time': message.time,
        })

    return {
        'messages': filtred
    }


@app.route("/install")
def install():
    """
    Создание базы данных и пользователя Joe
    :return: JSON {"ok": true}
    """
    db.create_all()
    joe = User(user='Joe', password='joe')
    db.session.add(joe)
    db.session.commit()
    return {"ok": True}


app.run()
