import requests


def send_message(username, password, text):
    """
    :param password:
    :param username:
    :param text:
    :return:
    """
    message = {'username': username, 'password': password, 'text': text}
    response = requests.post('http://127.0.0.1:5000/send', json=message)
    return response.status_code == 200


username = input('Введите имя: ')
password = input('Введите пароль: ')

while True:
    text = input('Введите сообщение: ')
    result = send_message(username, password, text)
    if result is False:
        print('Error')
