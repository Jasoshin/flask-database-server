<h1>Серверное приложение на Python (Flask + PostgreSQL)</h1>

<h2>Подготовка</h2>

<p>В config.py заполните учётные данные для доступа к вашей базе данных:</p>

```commandline
host = 'iP-адрес базы данных'
user = 'Ваше имя пользователя для доступа к базе данных'
password = 'Ваш пароль для доступа к базе данных '
db_name = 'Имя вашей базы данных'
```

<p>Установите необходимые библиотеки для запуска:</p>

```commandline
pip install -r requirements.txt
```

<p>Установите необходимые для корректной работы приложения СУБД PostgreSQL и Postman(опционально, для тестирования API), либо любую другую API-платформу</p>

<h2>Запуск</h2>

```commandline
python main.py
```

<h2>Usage</h2>

<p> Учётные данные, которые принимает сервер:

- username: имя пользователя, которое будет использоваться при регистрации.
- password: пароль для учетной записи пользователя.
- email: адрес электронной почты пользователя.</p>

<p>Важное замечание при создании пароля: 
должен иметь длину от 8 до 16 символов и содержать хотя бы одну цифру,
одну строчную букву, одну прописную букву и один специальный символ, также
не должен содержать пробелов. В противном случае - пароль не будет являться валидным для сервера и вернёт ошибку.</p>

Приложение позволяет использовать следующие API-вызовы:

|                                                 | Вводные данные<br/>для вызова                                                                                                                                                                                     | Выходные данные<br/>при успешном ответе| Выходные данные<br/>при ошибке                                               | Формат данных| Пример данных<br/>(успешных/неуспешных)                                                                                                                                                                                                                                                                                | 
|-------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------|------------------------------------------------------------------------------|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|  
| Приветственное сообщение<br/>на главной странице| GET /<br/>ip / домен корневого URL, где работает сервер: http://example.org/                                                                                                                                      | Welcome to my Flask App!               | None                                                                         | HTML-строка  | ```html<p>Welcome to my Flask App!</p>```                                                                                                                                                                                                                                                                              | 
| Регистрация <br/> нового пользователя           | POST /api/register<br/>Все учётные данные:<br/>```json{"username": <username>, "password": <password with a-zA-Z0-9 and specials (length from 8 to 16)>, "email": <email@example.com>}```                         | HTTP-статус: 200;<br/>Тело ответа      | HTTP-статус: 502;<br/>Ответ в json;<br/>в поле exception: описание ошибки    | JSON         | ```json{'status': 'success', 'message': 'User registered successfully'},200```<br/>```json{'status': 'exception','message': 'Exception('An error occurred during registration')'}, 502```                                                                                                                              | 
| Вход<br/>пользователя                           | POST /api/login<br/>Существующие email / username и password:<br/>```json{"username": <username>, "email": <email@example.com>, "password": <password>}```                                                        | HTTP-статус: 200;<br/>Тело ответа      | HTTP-статус: 502;<br/>Ответ в json;<br/>в поле exception: описание ошибки    | JSON         | ```json{'status': 'success', 'message': 'User logged successfully', 'token': token},200```<br/>```json{'status': 'exception','message': 'Exception('Invalid credentials')'}, 502```                                                                                                                                    | 
| Удаление<br/>пользователя                       | POST /api/user/delete<br/>Токен доступа существующего пользователя:<br/>```json{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}```                                                                            | HTTP-статус: 200;<br/>Тело ответа      | HTTP-статус: 403/502;<br/>Ответ в json;<br/>в поле exception: описание ошибки| JSON         | ```json{'status': 'success', 'message': 'User deleted successfully'},200```<br/>```json{'status': 'error', 'message': 'token invalid'},403```<br/>```json{'status': 'exception','message': 'Exception('An error occurred during user deletion')'}, 502```                                                              | 
| Получение списка<br/>всех пользователей         | POST /api/get_users<br/>Токен доступа существующего пользователя:<br/>```json{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}```                                                                              | HTTP-статус: 200;<br/>Тело ответа      | HTTP-статус: 403/502;<br/>Ответ в json;<br/>в поле exception: описание ошибки| JSON         | ```json{'id': 1, 'username': 'user1', 'email': 'user1@example.com'}, {'id': 2, 'username': 'user2', 'email': 'user2@example.com'}```<br/>```json{'status': 'error', 'message': 'token invalid'},403```<br/>```json{'status': 'exception','message': 'Exception('An error occurred during getting data users')'}, 502```| 
| Обновление данных<br/>пользователя              | POST /api/user/update<br/>Токен доступа и обновляемые username / email / password:<br/>```json{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...","key": <email@example.com>, "value": <new_email@example.com>}```| HTTP-статус: 200;<br/>Тело ответа      | HTTP-статус: 502;<br/>Ответ в json;<br/>в поле exception: описание ошибки    | JSON         | ```json{'status': 'success'}, 200```<br/>```json{'status': 'error', 'exception': 'Unsupported key type: only username, password, email'}, 502```<br/>```json{'error': 'exception','exception': 'token invalid'}, 403```                                                                                                | 

 