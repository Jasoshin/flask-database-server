import hashlib

import psycopg2


class DatabaseProps:
    """ Класс для хранения учётных данных используемой базы данных.

        Атрибуты:
        host (str | None): Используемый IP-адрес базы данных.
        db_name (str | None): Имя используемой базы данных.
        user (str | None): Учётные данные пользователя для доступа к базе данных.
        password (str | None): Используемый пароль для доступа к базе данных.
    """
    host: str | None = None
    db_name: str | None = None
    user: str | None = None
    password: str | None = None


class DatabaseManager:
    """ Класс для взаимодействия с подключенной базой данных.
    Происходит соединение и непосредственное управление.
    """
    def __init__(self, props: DatabaseProps):
        """ Инициализирует новое соединение с базой данных с
        использованием параметров props.

        :param props: Экземпляр класса DatabaseProps, который
        содержит все данные для подключения к базе данных.
        """
        self.connection = psycopg2.connect(
            host=props.host,
            user=props.user,
            password=props.password,
            database=props.db_name
        )
        self.connection.autocommit = True

    def __del__(self):
        """ Закрывает соединение с базой данных
         во время уничтожения экземпляра класса.
        """
        self.connection.close()

    def create_users_table(self):
        """ Создание таблицы при условии, что она ещё не существует.
        Указываются данные, которые будут созданы при регистрации с помощью SQL-запроса:
        1. Числовой идентификатор, который увеличивается для каждой новой записи.
        2. Уникальное имя пользователя(до 50 символов).
        3. Хэшируемый пароль пользователя(до 64 символов).
        4. Адрес электронной почты пользователя(до 100 символов).
        """
        query = """CREATE TABLE IF NOT EXISTS users(
                id serial PRIMARY KEY,
                username varchar(50) UNIQUE NOT NULL,
                pwd_hash varchar(64) NOT NULL,
                email varchar(100) UNIQUE NOT NULL);"""
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            print(query)

    def add_user(self, username, password_hash, email):
        """ Функция добавления нового пользователя с помощью
        предоставленных данных для регистрации
        с использованием SQL-запроса.

        :param username: Предоставленное имя пользователя.
        :param password_hash: Предоставленный пароль, который хэшируется.
        :param email: Предоставленный адрес электронной почты.
        """
        query = f"""INSERT INTO users(username, pwd_hash, email)
                 VALUES ('{username}', '{password_hash}', '{email}');"""
        print(query)

        with self.connection.cursor() as cursor:
            cursor.execute(query)

    def update_userdata(self, user_id, key, value):
        """ Функция обновления данных пользователя.
        Обновляет определенное поле данных (одно из атрибутов)
        с помощью SQL-запроса, например: почту или пароль.

        :param user_id: Id пользователя, который требуется обновить.
        :param key: Название поля в таблице базы дынных, который требуется обновить.
        :param value: Новое значение для указанного поля.
        """
        query = f"""
        UPDATE users SET {key} = '{value}' WHERE id = '{user_id}';"""
        with self.connection.cursor() as cursor:
            cursor.execute(query)

    def delete_user(self, user_id):
        """ Функция удаления определённого пользователя
        с помощью SQL-запроса.

        :param user_id: Id пользователя.
        """
        query = f"""
        DELETE FROM users WHERE id = '{user_id}';"""
        print(query)

        with self.connection.cursor() as cursor:
            cursor.execute(query)

    def is_username_exists(self, username):
        """ Функция проверки на существование
        какого-либо имени пользователя с помощью SQL-запроса.

        :param username: Предполагаемое имя пользователя.
        :return: Возвращает указанное имя пользователя,
        если такой существует.
        """
        query = f"""
        SELECT count(*) FROM users WHERE username = '{username}';"""

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

        return row[0] > 0

    def is_email_exists(self, email):
        """ Функция проверки на существование
        какого-либо адреса электронной почты
        с помощью SQL-запроса.

        :param email: Предполагаемый адрес электронной почты.
        :return: Возвращает указанный адрес электронной почты,
        если такой существует.
        """
        query = f"""
        SELECT count(*) FROM users WHERE email = '{email}';"""

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

        return row[0] > 0

    def get_user_by_username(self, username):
        """ Функция получения информации о пользователе
        с помощью его имени пользователя с использованием
        SQL-запроса.

        :param username: Предполагаемое имя пользователя.
        :return: Возвращает данные указанного пользователя.
        """
        query = f"""
        SELECT * FROM users WHERE username = '{username}';"""

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

        return row

    def get_user_by_email(self, email):
        """ Функция получения информации о пользователе
        с помощью его адреса электронной почты с использованием
        SQL-запроса.

         :param email: Предполагаемый адрес электронной почты.
        :return: Возвращает данные указанного пользователя.
        """
        query = f"""
        SELECT * FROM users WHERE email = '{email}';"""

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

        return row

    def get_users(self):
        """ Функция получения информации о
        всех пользователях зарегистрированных
        в базе данных.

        :return: Возвращает данные о каждом пользователе.
        """
        query = f"""
        SELECT * FROM users;"""

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        return rows
