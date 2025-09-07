# [Auth System](https://github.com/VictorVolkov7/auth_system)


## Оглавление:

- [Технологии](#технологии)
- [Описание проекта](#Описание-проекта)
- [Архитектура и структура базы данных](#архитектура-и-структура-базы-данных)
- [Установка и запуск проекта](#установка-и-запуск-проекта)
- [Работа с API](#работа-с-api)
- [Пример прав доступа](#пример-прав-доступа)
- [Примеры запросов](#примеры-запросов)
- [Демонстрация работы системы](#демонстрация-работы-системы)
- [Автор](#Автор)


## Технологии:

- Python 3.12

С использованием библиотек/фреймворков:
- Django 5.2.5
- Django REST framework 3.16.1
- drf-spectacular 0.28.0
- PostgreSQL
- Docker + Docker Compose
- bcrypt (хеширование паролей)


## Описание проекта:

Собственная система аутентификации и авторизации с ролевой моделью доступа (RBAC) на базе Django и DRF.

1. Приложение реализует:
   - Регистрацию и управление пользователями
   - Аутентификацию через сессии (cookie-based)
   - Ролевую авторизацию на уровне бизнес-объектов
   - Управление правами доступа через AccessRoleRule
   - Минимальные mock-объекты бизнес-приложения для демонстрации работы прав доступа
2. Особенности:
   - Мягкое удаление пользователей
   - Кастомный middleware для работы с сессиями
   - Кастомный DRF permissions для проверки ролей и прав на объекты
   - Администратор может управлять правилами доступа через API


## Архитектура и структура базы данных:

<table>
    <tr>
        <th>Модель</th>
        <th>Описание</th>
    </tr>
    <tr>
        <td>User</td>
        <td>Пользователь системы. Содержит email, имя, роль, статус активности</td>
    </tr>
    <tr>
        <td>Role</td>
        <td>Роль пользователя (Администратор, Пользователь, Редактор)</td>
    </tr>
    <tr>
        <td>BusinessElement</td>
        <td>Бизнес-объекты, к которым применяется доступ (товары, пользователи, заказы, правила)</td>
    </tr>
    <tr>
        <td>AccessRoleRule</td>
        <td>Права роли на бизнес-объекты (read, create, update, delete и версии _all)</td>
    </tr>
    <tr>
        <td>Session</td>
        <td>Сессии пользователей с cookie session_key и временем жизни</td>
    </tr>
</table>

### Логика доступа
- _permission — действия над объектами, принадлежащими пользователю
- _all_permission — действия над всеми объектами
- Пользователь без нужного разрешения получает 403 Forbidden
- Незалогиненный пользователь получает 401 Unauthorized

## Установка и запуск проекта

### Запуск проекта:

* Форкните/Клонируйте репозиторий и перейдите в него:
```
git clone https://github.com/VictorVolkov7/auth_system
```

* Создайте и активируйте виртуальное окружение:
```
poetry shell
```
Установите зависимости:
```
poetry install
```

* Создайте **.env** файл в корневой папке проекта. В нем должны быть указаны переменные из файла **.env.example**.
```ini
#Project settings
DEBUG=True
USE_DEBUG_TOOLBAR=True

# Django settings
DJANGO_SECRET_KEY=django_secret_key

# PostgreSQL settings
POSTGRES_DB=db_name
POSTGRES_USER=psql_username
POSTGRES_PASSWORD=psql_password
POSTGRES_HOST=local_ip
POSTGRES_PORT=port_for_db
```

* Создайте и примените миграции:
```
python manage.py makemigrations
python manage.py migrate

или

make migrate
```

* Воспользуйтесь командой для установки русского языка:
```
django-admin compilemessages

или

make compile-mes
```

* ЗАПУСК BACKEND-ЧАСТИ: Запустите сервер (воспользуйтесь командами или настройте запуск Django сервера в настройках.):

```
python manage.py runserver

или

make run
```

Другие команды в проекте можете посмотреть в Makefile.

Таким образом можно работать с backend-частью локально для отладки.

После запуска сервера. Вы сможете перейти на сайт с документацией http://127.0.0.1:8000/api/docs/ (если сервер запущен локально), и начать пользоваться всеми API методами проекта. 

Также вы можете схему данных .yaml файлом по адресу http://127.0.0.1:8000/api/schema/ (если сервер запущен локально).

### Либо с помощью Docker
* Измените файл **.env** в корневой папке проекта, заменив значение в строчке **"POSTGRES_HOST"** на Ваше название 
контейнера с базой данных:
```ini
#Project settings
DEBUG=True
USE_DEBUG_TOOLBAR=True

# Django settings
DJANGO_SECRET_KEY=django_secret_key

# PostgreSQL settings
POSTGRES_DB=db_name
POSTGRES_USER=psql_username
POSTGRES_PASSWORD=psql_password
POSTGRES_HOST=container_name(default:'db')
POSTGRES_PORT=port_for_db
```

* ЗАПУСК BACKEND-ЧАСТИ:: Воспользуйтесь командами:
```
docker compose build (для создания оптимального билда проекта).

docker compose up -d (для запуска docker compose контейнера (флаг -d запуск в фоновом режиме)).
```
- После старта будут выполнены миграции и компиляция сообщений:
  - makemigrations
  - migrate
  - compilemessages
  - collectstatic

Сервис будет доступен по вашему локальному адресу с портом 8000. Документация **(см. выше)**.

## Работа с API
### 1. Пользователи
<table>
    <tr>
        <th>API эндпоинт</th>
        <th>Метод</th>
        <th>Описание</th>
    </tr>
    <tr>
        <td>/users/register/</td>
        <td>POST</td>
        <td>Регистрация нового пользователя</td>
    </tr>
    <tr>
        <td>/users/login/</td>
        <td>POST</td>
        <td>Вход, создание сессии</td>
    </tr>
    <tr>
        <td>/users/logout/</td>
        <td>POST</td>
        <td>Выход, деактивация сессии</td>
    </tr>
    <tr>
        <td>/users/profile/</td>
        <td>GET, PUT, PATCH, DELETE</td>
        <td>Просмотр, редактирование и мягкое удаление аккаунта</td>
    </tr>
</table>

### 2. Бизнес-объекты (mock)
<table>
    <tr>
        <th>API эндпоинт</th>
        <th>Метод</th>
        <th>Доступ</th>
        <th>Описание</th>
    </tr>
    <tr>
        <td>/products/</td>
        <td>GET, POST</td>
        <td>Доступ по AccessRoleRule</td>
        <td>Просмотр и создание объектов</td>
    </tr>
    <tr>
        <td>/products/id/</td>
        <td>GET, PUT, PATCH, DELETE</td>
        <td>Доступ по AccessRoleRule и владельцу объекта</td>
        <td>Просмотр, редактирование и удаление объектов</td>
    </tr>
</table>

### 3. Управление AccessRoleRule (для админов)
<table>
    <tr>
        <th>API эндпоинт</th>
        <th>Метод</th>
        <th>Описание</th>
    </tr>
    <tr>
        <td>/users/access-rules/</td>
        <td>GET</td>
        <td>Получить список правил</td>
    </tr>
    <tr>
        <td>/users/access-rules/id/</td>
        <td>GET, PUT, PATCH, DELETE</td>
        <td>Просмотр, редактирование и удаление правил</td>
    </tr>
</table>

## Пример прав доступа
```json
{
  "role": 2,
  "element": 1,
  "read_permission": true,
  "read_all_permission": false,
  "create_permission": true,
  "update_permission": true,
  "update_all_permission": false,
  "delete_permission": true,
  "delete_all_permission": false
}
```

## Примеры запросов

#### Логин:
```bash
curl -X POST http://localhost:8000/users/login/ \
-H "Content-Type: application/json" \
-d '{"email":"user@example.com","password":"password123"}'
```

#### Получение списка продуктов:
```bash
curl -X GET http://localhost:8000/products/ \
-H "Cookie: session_key=<session_key>"
```

## Демонстрация работы системы

- Пользователь с ролью «Пользователь» видит/редактирует только свои объекты
- Редактор видит/редактирует все объекты, но не может удалять чужие
- Администратор видит/редактирует/удаляет все объекты и может менять правила доступа
- Попытка доступа к чужим объектам без _all_permission → 403
- Незалогиненный доступ → 401

## Автор
[Volkov Victor](https://github.com/VictorVolkov7/)