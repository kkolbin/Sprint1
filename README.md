# Документация к REST API проекта Pereval

## Описание задачи
Проект Pereval создан для реализации REST API, предназначенного для управления перевалами в горах. 
Каждый перевал имеет определенные координаты, уровень сложности и может содержать изображения. 
Пользователи могут добавлять новые перевалы, редактировать информацию о них, а также получать список перевалов, 
отправленных пользователем с определенной почтой.

## Методы REST API

### 1. POST /api/submitData/
Этот метод позволяет добавить новый перевал в базу данных.

#### Входные данные
Метод принимает следующие данные в формате JSON:
- "email": электронная почта пользователя (строка),
- "fam": фамилия пользователя (строка),
- "name": имя пользователя (строка),
- "otc": отчество пользователя (строка, опционально),
- "phone": номер телефона пользователя (строка),
- "latitude": широта перевала (число),
- "longitude": долгота перевала (число),
- "height": высота перевала (число),
- "spring": уровень сложности весной (строка),
- "summer": уровень сложности летом (строка),
- "autumn": уровень сложности осенью (строка),
- "winter": уровень сложности зимой (строка),
- "beauty_title": тип объекта (строка),
- "title": название объекта (строка),
- "other_titles": другое название (строка, опционально),
- "connect": подключение (строка, опционально).

#### Выходные данные
В случае успешного добавления перевала в базу данных, метод вернет следующий JSON-объект:
{
"status": 200,
"message": "Успех",
"id": "id перевала"
}

В случае ошибки сервера:
{
"status": 500,
"message": "Ошибка при выполнении операции",
"id": null
}

Если данные не прошли валидацию:
{
"status": 400,
"message": "Сервер не смог обработать некоторые поля",
"id": null
}

### 2. GET /api/submitData/{id}
Этот метод позволяет получить информацию о перевале по его идентификатору.

#### Входные данные
Идентификатор перевала (число).

#### Выходные данные
Информация о перевале в формате JSON.

### 3. PATCH /api/submitData/{id}
Этот метод позволяет отредактировать существующий перевал в базе данных, если он имеет статус "new".

#### Входные данные
Идентификатор перевала и данные для редактирования.

#### Выходные данные
В случае успешного редактирования:
{
"state": 1,
"message": "Данные изменены"
}

Если редактирование не удалось:
{
"state": 0,
"message": "При статусе: <статус перевала>, редактирование невозможно."
}

### 4. GET /api/submitData/?user__email=<email>
Этот метод позволяет получить список всех перевалов, отправленных пользователем с указанной электронной почтой.
Список зависимостей в файле requirements.txt

#### Входные данные
Электронная почта пользователя.

#### Выходные данные
Список перевалов в формате JSON.

## Конфигурация базы данных

Для подключения к базе данных используются следующие переменные окружения:

- `FSTR_DB_HOST`: путь к базе данных;
- `FSTR_DB_PORT`: порт базы данных;
- `FSTR_DB_NAME`: имя базы данных;
- `FSTR_DB_LOGIN`: логин для подключения к базе данных;
- `FSTR_DB_PASS`: пароль для подключения к базе данных.

## Установка и запуск проекта

1. Клонируйте репозиторий:

git clone https://github.com/kkolbin/Pereval.git


2. Перейдите в каталог проекта:

cd Pereval


3. Установите зависимости:

pip install -r requirements.txt


4. Установите переменные окружения в файле `.env`.

5. Выполните миграции:

python manage.py migrate



6. Запустите сервер:

python manage.py runserver



## Пример использования API

### Добавление нового перевала

curl -X POST http://localhost:8000/submitData -H "Content-Type: application/json" -d '{"email": "example@example.com", 
"fam": "Иванов", "name": "Иван", "otc": "Иванович", "phone": "123456789", "latitude": 55.7558, "longitude": 37.6176, 
"height": 1500, "spring": "easy", "summer": "medium", "autumn": "hard", "winter": "extreme", "beauty_title": "lake", 
"title": "Lake Baikal", "other_titles": "Older title", "connect": "by car"}'



### Получение информации о перевале по идентификатору

curl -X GET http://localhost:8000/submitData/1



### Редактирование информации о перевале по идентификатору

curl -X PATCH http://localhost:8000/submitData/1 -H "Content-Type: application/json" -d '{"latitude": 55.7558, 
"longitude": 37.6176, "height": 1600, "spring": "easy", "summer": "medium", "autumn": "hard", "winter": "extreme",
"beauty_title": "mountain", "title": "Mount Everest", "other_titles": "Older title", "connect": "by foot"}'



### Получение списка перевалов, отправленных пользователем с определенной почтой

curl -X GET http://localhost:8000/submitData/?user__email=example@example.com

## Автор
Автор: Константин
Email: kkolbin@gmail.com
GitHub: [kkolbin](https://github.com/kkolbin)