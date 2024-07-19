import hashlib

from components.AuthValidation import pass_email, pass_username
from components.DatabaseManager import DatabaseManager as DBManager


def authenticate(db: DBManager, login, password):
    """ Реализуется аутентификация пользователя с проверкой логина(почта, имя пользователя) и пароля,
    которые хранятся в базе данных. Функция проверяет - является ли предоставленный логин
    именем пользователя или электронной почтой, затем проверяет - существует ли пользователь в базе данных.
    И если пользователь существует: функция сравнивает предоставленный пароль с сохранённым хэшем.

    :param db: Менеджер для взаимодействия с БД.
    :param login: Учётные данные для входа(электронная почта или имя пользователя).
    :param password: Пароль для аутентификации.
    :return: Возвращение идентификатора, в случае успешной аутентификации.
    :raise: Исключения в случае, если тип входа не распознан или неверный пароль,
    или пользователь не существует.
    """
    if pass_email(login):
        email = login
        if not db.is_email_exists(email):
            raise Exception('Email entry is not found')
        user_data = db.get_user_by_email(email)
    elif pass_username(login):
        username = login
        if not db.is_username_exists(username):
            raise Exception('Username entry is not found')
        user_data = db.get_user_by_username(username)
    else:
        raise Exception('Invalid login')

    pwd_hash = user_data[2]
    if pwd_hash != hashlib.sha256(password.encode('utf-8')).hexdigest():
        raise Exception('Invalid login or password')

    return user_data[0]
