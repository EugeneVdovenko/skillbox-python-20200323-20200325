from PyQt5 import QtWidgets, QtCore
import window
import requests
from _datetime import datetime


class MessengerApp(QtWidgets.QMainWindow, window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.after = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(1000)

        self.pushButton.pressed.connect(self.button_pushed)

    def button_pushed(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        text = self.textEdit.toPlainText()

        self.send_message(username, password, text)
        self.textEdit.setText('')
        self.textEdit.repaint()

    def send_message(self, username, password, text):
        """
        :param self
        :param password:
        :param username:
        :param text:
        :return:
        """
        message = {'username': username, 'password': password, 'text': text}
        try:
            response = requests.post('http://127.0.0.1:5000/send', json=message)
            if response.status_code == 401:
                self.show_text('Bad password')
            elif response.status_code != 200:
                self.show_text('Connection error')
        except:
            self.show_text('Connection error')

    def update_messages(self):
        try:
            response = requests.get(
                'http://127.0.0.1:5000/history',
                params={'after': self.after})

            data = response.json()
            for message in data['messages']:
                self.print_message(message)
                self.after = message["time"]

        except:
            print('Connection error')

    def print_message(self, message):
        text = message['text']
        nick = message['username']
        timestamp = float(message['time'])

        ct = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
        self.show_text(f'{ct} {nick}\n{text}\n\n')

    def show_text(self, text):
        self.textBrowser.append(text)
        self.textBrowser.repaint()


app = QtWidgets.QApplication([])
messenger = MessengerApp()
messenger.show()
app.exec_()
