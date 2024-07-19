import re

from components.AuthValidation import pass_username, pass_password, pass_email
from components.DatabaseManager import DatabaseManager as DBManager
import hashlib


class RegistrationProps:
    """ Класс для хранения свойств регистрации нового пользователя.

        Атрибуты:
        username (str | None): Предпочитаемое имя пользователя для нового пользователя.
        password (str | None): Предпочитаемый пароль для нового пользователя.
        email (str | None): Электронный адрес ассоциирующийся с новым пользователем.
        """
    username: str | None = None
    password: str | None = None
    email: str | None = None


def register_user(db: DBManager, props: RegistrationProps):
    """ Реализация регистрации нового пользователя в базе данных.
    В функции происходит проверка соответствия:
    1. Если пользователя с предоставленными данными(имя пользователя, электронная почта) не существует.
    2. Соответствуют ли предоставленные данные уже предопределённым критериям базы данных.

    :param db: Менеджер для взаимодействия с базой данных.
    :param props: Экземпляр, который содержит данные пользователя.
    """
    if not pass_username(props.username):
        raise Exception('Username is not valid')
    if not pass_password(props.password):
        raise Exception('Password is not valid')
    if not pass_email(props.email):
        raise Exception('Email is not valid')

    if db.is_username_exists(props.username):
        raise Exception('Registered username already exists')
    if db.is_email_exists(props.email):
        raise Exception('Registered email already exists')

    password_hash = hashlib.sha256(props.password.encode('utf-8')).hexdigest()
    db.add_user(
        props.username,
        password_hash,
        props.email
    )
