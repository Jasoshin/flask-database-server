import datetime
import hashlib
import json

import config
from api.registration import register_user, RegistrationProps
from api.authentication import authenticate
from components.AuthValidation import pass_username, pass_email, pass_password
from components.DatabaseManager import DatabaseManager as DBManager, DatabaseProps

from flask import Flask, render_template, request, redirect, url_for

tokens = dict()


def token_exists(token):
    """ Функция проверяет, существует ли токен в созданном выше словаре,
    для определения вызываемого пользователя.

    :param token: Токен доступа для проверки
    :return: Возвращает Id пользователя, если такой существует.
    """
    for user_id, user_token in tokens.items():
        if user_token == token:
            return user_id
    return None

# Установка связи с указанной в config.py базой данных
props = DatabaseProps()
props.host = config.host
props.db_name = config.db_name
props.user = config.user
props.password = config.password
db = DBManager(props)

app = Flask(__name__) # Создаём экземпляр серверного приложения Flask.

#Декоратор во Flask, связывающий URL-адрес ('/') с функцией-обработчиком (index()).
@app.route('/')
def index():
    """ Функция отображения приветственного сообщения на главной странице.

    :return: Возвращает HTML-строку с приветственным сообщением.
    """
    return '''
    <p>Welcome to my Flask App!</p>
    '''


@app.route('/api/register', methods=['POST'])
def register():
    """ Функция регистрации нового пользователя.
    Происходит попытка принять json-данные с указанными параметрами
    пользователя. При успешной регистрации возвращается
    соответствующий статус, в противном случае - исключение с
    информацией об ошибке.

    :return: Возвращает результат и HTTP-статус.
    """
    try:
        data = request.json

        reg_props = RegistrationProps()
        reg_props.username = data['username']
        reg_props.password = data['password']
        reg_props.email = data['email']

        register_user(db, reg_props)
    except Exception as e:
        return {'exception': f'{repr(e)}'}, 502
    return {
        'status': 'success',
        'message': 'User registered successfully'
    }


@app.route('/api/login', methods=['POST'])
def login():
    """ Функция входа пользователя.
    Происходит попытка принять json-данные, которые могут
    содержать параметры пользователя (username и emai, пароль).
    При успешной аутентификации создаётся и возвращается токен
    доступа, в противном случае - исключение с
    информацией об ошибке.

    :return: Возвращает результат и HTTP-статус.
    """
    try:
        data = request.json

        password = data['password']

        user_id = -1

        if 'username' in data:
            username = data['username']
            user_id = authenticate(db, username, password)
        if 'email' in data:
            email = data['email']
            user_id = authenticate(db, email, password)

        token = hashlib.sha256(f'{user_id}+{password}+{datetime.datetime.now()}'.encode('utf-8')).hexdigest()

        tokens[user_id] = token

        return {
            'status': 'success',
            'message': 'User logged successfully',
            'token': token
        }
    except Exception as e:
        return {'exception': f'{repr(e)}'}, 502


@app.route('/api/user/delete', methods=['POST'])
def delete_user():
    """ Функция удаления пользователя.
    Происходит попытка принять json-данные с токеном доступа.
    Если токен действителен и существует - происходит удаление
    пользователя, а в противном случае - возвращает исключение
    с информацией об ошибке.

    :return: Возвращает результат и HTTP-статус.
    """
    try:
        data = request.json
        token = data['token']

        user_id = token_exists(token)
        if not user_id:
            return {
                'status': 'error',
                'message': 'token invalid'
            }, 403
        db.delete_user(user_id)

        return {
            'status': 'success',
            'message': 'user deleted successfully'
        }, 200
    except Exception as e:
        return {
            'status': 'exception',
            'message': f'{repr(e)}'}, 502


@app.route('/api/get_users', methods=['POST'])
def get_users():
    """ Функция получения списка всех пользователей.
    Происходит попытка принять json-данные с токеном доступа.
    Если токен действителен и существует - происходит вывод
    списка всех пользователей, а в противном случае - возвращает исключение
    с информацией об ошибке.

    :return: Возвращает результат с HTTP-статусом.
    """
    try:
        data = request.json
        token = data['token']

        if not token_exists(token):
            return {
                'status': 'error',
                'message': 'token invalid'}, 403
        users = db.get_users()
        return json.dumps(users), 200
    except Exception as e:
        return {
            'status': 'exception',
            'message': f'{repr(e)}'}, 502


@app.route('/api/user/update', methods=['POST'])
def update_user():
    """ Функция обновления данных о пользователе.
    Происходит попытка принять json-данные с токеном доступа
    и ключом-значением содержащим один из параметров
    пользователя (username, email, password). Пароль также
    хэшируется перед сохранением в базу данных.
    Затем идёт проверка валидности данных и возвращение
    соответствующего статуса.

    :return: Возвращает данные со статусом операции и HTTP-статус при успехе,
             или словарь с ошибкой и HTTP-статус при неудаче.
    """
    try:
        data = request.json
        token = data['token']
        user_id = token_exists(token)
        if not user_id:
            return {
                'status': 'error',
                'exception': 'token invalid'}, 403

        key = data['key']
        value = data['value']

        if key != 'username' and key != 'password' and key != 'email':
            return {
                'status': 'error',
                'exception': 'Unsupported key type: only username, password, email'}, 502
        if key == 'username':
            if not pass_username(value):
                return {
                    'status': 'error',
                    'exception': 'Invalid username value'}, 502
        elif key == 'password':
            if not pass_password(value):
                return {
                    'status': 'error',
                    'exception': 'Invalid password value'}, 502
            else:
                key = 'pwd_hash'
                value = hashlib.sha256(value.encode('utf-8')).hexdigest()
        elif key == 'email':
            if not pass_email(value):
                return {
                    'status': 'error',
                    'exception': 'Invalid email value'}, 502

        db.update_userdata(user_id, key, value)
        return {'status': 'success'}, 200
    except Exception as e:
        return {'exception': f'{repr(e)}'}, 502

# Основной скрипт, который выполняет инициализацию базы данных.
# Создаёт таблицу пользователей и запускает серверное приложение Flask.
# Отключаем режим отладки в реальном времени, устанавливаем общедоступный хост и ставим HTTP порт 80.
if __name__ == '__main__':
    db.create_users_table()
    app.run(debug=False, host='0.0.0.0', port=80)

