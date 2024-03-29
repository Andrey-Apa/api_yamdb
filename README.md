# Проект YaMDb API
Это групповой учебный проект Яндекс-Практикум
## Описание

Проект YaMDb позволяет через простые запросы API собирать отзывы, оценки и комментарии пользователей на различные произведения хранящиеся в базе данных.

## Технологии
- Python 3.7.9 и выше
- Django 3.2
- Django REST Framework 3.12.4
- SimpleJWT 4.7.2
- Django filter 22.1
- Dotenv 0.21.1

## Содержание .env 
- SECRET_KEY — секретный ключ

## Запуск проекта
Клонировать репозиторий:
```bash
git clone git@github.com:Andrey-Apa/api_yamdb.git
```
Cоздать и активировать виртуальное окружение:
```bash
-для Windows
python -m venv venv
-для Linux, MacOs:
python3 -m venv venv
```
```bash
-для Windows
. venv/Scripts/activate
-для Linux, MacOs:
source env/bin/activate
```
Обновите pip
```bash
-для Windows
python -m pip install --upgrade pip
-для Linux, MacOs:
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```bash
pip install -r requirements.txt
```
Выполнить миграции:
```bash
cd api_yamdb
```
```bash
-для Windows
python manage.py migrate
-для Linux, MacOs:
python3 manage.py migrate
```
Запустить проект:
```bash
-для Windows
python manage.py runserver
-для Linux, MacOs:
python3 manage.py migrate
```
Импорт тестовых данных из csv-файлов в дирректории static/data/ в Базу Данных командой:
```bash
python manage.py csv_import
```
Обратите внимание, команда вводится после создания и применения миграций. В базе данных не должно быть записей с id такими же как в тестовых данных.

Создайте суперпользователя:
```bash
-для Windows
python manage.py createsuperuser
-для Linux, MacOs:
python3 manage.py createsuperuser
```
Username (leave blank to use 'user'): # Придумайте логин (например, admin)
Email address: # укажите почту
Password: # придумайте пароль
Password (again): # повторите пароль

## Документация к API
Подробная документация приведена по ссылке ниже:
http://127.0.0.1:8000/redoc

## Алгоритм регистрации пользователей
1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.
2. YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
3. Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле (описание полей — в документации).

## Примеры запросов
- GET http://127.0.0.1:8000/api/v1/titles/

Возвращает список всех произведений.
```
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": []
    }
]
```
- POST http://127.0.0.1:8000/api/v1/titles/

Создание нового объекта произведения (доступно только админу, суперюзеру).
В теле запроса можно передвать переменные:
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Пример ответа:
```
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
              {}
    ],
    "category": {
        "name": "string",
        "slug": "string"
    }
}
```
- GET http://127.0.0.1:8000/api/v1/titles/{titles_id}/

Возвращает информацию о конкретном произведении по id (доступно без токена)
Пример ответа:
```
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
              {}
    ],
    "category": {
        "name": "string",
        "slug": "string"
    }
}
```
- PATCH, DELETE http://127.0.0.1:8000/api/v1/titles/{titles_id}/

Частичное изменение или удаление конкретного объекта (доступно только админу, суперюзеру)
Пример запроса для PATCH:
```
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
```
- GET http://127.0.0.1:8000/api/v1/titles/1/reviews/

Возвращает список всех отзывов (доступно без токена)
Пример ответа:
```
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
                {}
    ]
}
```
- POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/

Добавление нового отзыва. Пользователь может оставить только один отзыв на произведение и поставить оценку в диапазоне от 1 до 10 (доступно аутентифицированным пользователям)
Пример запроса:
```
{
  "text": "string",
  "score": 1
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
- GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/

Возварщает список всех комментариев к отзыву по id произведения и отзыва (доступно без токена)
Пример ответа:
```
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
                {}
    ]
}
```
- POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/

Добавление нового комментария к отзыву (доступно аутентифицированным пользователям)
Пример запроса:
```
{
  "text": "string"
}
```
Возвращает индекс и текст комментария, а также имя автора и дату публикации:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2023-01-28T22:15:22Z"
}
```

## Над проектом работали

- Андрей Грицай - https://github.com/Netsky-29
- Максим Бойко - https://github.com/Boikomp
- Андрей Апашкин - https://github.com/Andrey-Apa

## License

MIT

**Free Software, Not for commercial use!**