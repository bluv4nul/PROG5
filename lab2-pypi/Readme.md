# Лабораторная работа 3: Разработка REST API для отслеживания курсов валют (FastAPI + SQLAlchemy)

## Цель работы
Разработать асинхронное веб-приложение (REST API) с использованием фреймворка FastAPI и библиотеки SQLAlchemy (в качестве ORM) для взаимодействия с базой данных SQLite. Приложение должно предоставлять функционал регистрации пользователей и подписки на отслеживание актуальных курсов валют, получаемых от Центрального банка РФ.

## Структура проекта

```
|- db - Управление базой данных 
|- models - Модели базы данных 
|- schemas - Pydantic модели 
|- routers - Ендпоинты веб-приложения 
|- services - Дополнительные сервисы для работы веб-приложения 
|
|- app.py - Освовной файл приложения
|- Readme.md - Описание лабораторной (Отчет)
|- requirements.txt - Файл с зависимостями 
```

## База данных. SQLAlchemy.

В данной работе я использовал асинхронный вариант работы с SQLAlchemy для взаимодействия с DB.

В файле ./models/models.py находятся модели базы данных, а именно:

- User [id, username, email, created_at]
- Currency [id, code, name, value]
- Subscription [id, user_id, currency_id]

Организована связь "один ко многим" от таблиц User и Currency  к таблице Subscription.

В папке ./servies/ есть файлы, начинающиеся на "crud_". Так я называл файлы, отвечающие за взаимодействие с базой данных. Таких файла 3 - для каждой таблицы. 

**crud_user.py:**
```python
async def create_user(*args, *kwrgs) #создание пользователя
async def get_users(*args, *kwrgs) #получение пользователей
async def get_user_by_id_details(*args, *kwrgs) #получение информации о пользователе
async def delete_user_by_id(*args, *kwrgs) #удаление пользователя
async def update_user(*args, *kwrgs) #изменение пользователя
```

**crud_currency.py:**
```python
async def get_currencies(*args, *kwrgs) #вовзращает текущие курсы валют из БД
async def update_currencies(*args, *kwrgs) #Обращается к API(через функцию get_currencies_from_api) и обновляет курсы
```

**crud_subscription.py:**
```python
async def create_subscription(*args, *kwrgs) #Создает подписку
async def delete_subscription(*args, *kwrgs) #Удаляет подписку
```



## Api. FastAPI. Pydantic модели.

### Модели ответов

В папке ./schemas можно найти файлы с Pydantic моделями для FastAPI. Для каждой таблицы в базе данных свой файл с моделями ответа.

**user_schema.py:**
```python
class UserCreate(BaseModel) #для создания пользователя
class UserRead(BaseModel)  #для получение информации о пользователе (без валют)
class UserDetailRead(BaseModel) #получение полной информации о пользователе
class UserUpdate(BaseModel) #обновление пользователя
```

**currencies.py:**
```python
class CurrencySchema(BaseModel)  #информация о валюте
```

**subscription_schema.py:**
```python 
class SubscriptionCreate(BaseModel) #Создание подписки
class SubscriptionRead(BaseModel) #Чтение подписки
```


### Маршрутизация

В папке ./routers реализованы файлы с маршрутизацией.

**users.py:**
```
- POST /users/ - создание пользователя
- GET /users/ - получение списка всех пользователей
- GET /users/{user_id}/ - получение информации о пользователе и о валютах на которые он подписан
- PUT /users/{user_id}/ - изменение информации о пользователе
- DELETE /users/{user_id}/ - удаление пользователя
```

**currencies.py:**
```
- GET /currencies/ - получение информации о валютах
- UPDATE /currencies/ - обновление информации о валютах 
```

**subscription.py:**
``` 
- POST /subscription/ - добавление подписки
- DELETE /subscription/ - удаление подписки
```
