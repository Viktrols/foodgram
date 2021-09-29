![yamdb_workflow](https://github.com/Viktrols/foodgram-project-react/actions/workflows/backend.yml/badge.svg?branch=master)


[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)


# Foodgram - сайт с рецептами
Foodgram - сервис для публикации рецептов. Авторизованные пользователи могут подписываться на понравившихся авторов, добавлять рецепты в избранное, в покупки, скачать список покупок.
Неавторизованным пользователям доступна регистрация, авторизация, просмотр рецептов других авторов.

## Подготовка и запуск проекта
### Склонировать репозиторий на локальную машину:
```
git clone https://github.com/Viktrols/foodgram-project-react
```
## Для работы с удаленным сервером (на ubuntu):
### Выполните вход на свой удаленный сервер

### Установите docker на сервер:
```
sudo apt install docker.io 
```
### Установите docker-compose на сервер:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
### Локально отредактируйте файл infra/nginx.conf и в строке server_name впишите свой IP
### Скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```
### На сервере создайте файл .env (nano .env) и заполните переменные окружения (или создайте этот файл локально и скопируйте файл по аналогии с предыдущим пунктом):
```
SECRET_KEY=<секретный ключ проекта django>

DB_ENGINE=django.db.backends.postgresql
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=db
DB_PORT=5432

```
### Создайте на сервере файл pg.env для работы с контейнером postgres и поместите в него значения переменных окружения:
```
POSTGRES_PASSWORD=<пароль для базы данных> - обязательный параметр
DB_NAME=<название базы данных> - необязательный параметр (по умолчанию будет postgres)
POSTGRES_USER=<имя пользователя> - необязательный параметр (по умолчанию будет postgres)
```
### На сервере соберите docker-compose:
```
sudo docker-compose up -d --build
```
### После успешной сборки на сервере выполните команды (только после первого деплоя):
#### Соберите статические файлы:
```
sudo docker-compose exec backend python manage.py collectstatic --noinput
```
#### Применитe миграции:
```
sudo docker-compose exec backend python manage.py migrate --noinput
```
#### Загрузите ингридиенты в базу данных (не обязательно)
```
sudo docker-compose exec backend python manage.py loaddata fixtures/ingredients.json
```
#### Создать суперпользователя Django:
```
sudo docker-compose exec backend python manage.py createsuperuser
```
### Проект будет доступен по вашему IP
### Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
```
DOCKER_PASSWORD=<пароль от DockerHub>
DOCKER_USERNAME=<имя пользователя>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

TG_CHAT_ID=<ID чата, в который придет сообщение>
TELEGRAM_TOKEN=<токен вашего бота>
```
## Workflow состоит из трёх шагов:
- Сборка и публикация образа бекенда на DockerHub.
- Автоматический деплой на удаленный сервер.
- Отправка уведомления в телеграм-чат.
## Для ревью проект будет доступен по адресу http://84.201.163.135
### Вход на сайт/в админку:
```
nikita@reviewer.ru
test0101
```
### Образы доступны на DockerHub: [бекенд](https://hub.docker.com/repository/docker/viktrols/foodgram) и [фронтенд](https://hub.docker.com/repository/docker/viktrols/foodgram-frontend)

P.S. Если у вас другая ОС и не все команды из вышеперечисленных работают, вы всегда можете воспользоваться [гуглом](https://www.google.com/), вы ж программист! (даже если и начинающий)
