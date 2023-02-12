# Телеграм-бот с уведомлениями

Это чат бот, который отсылает уведомления о статусе проверки уроков
на обучающей платформе Devman
## Запуск:

### 1. Копируем содержимое проекта себе в рабочую директорию
```
git clone <метод копирования>
```

### 2. Устанавливаем библиотеки:
```
pip install -r requirements.txt
```

### 3. Для хранения переменных окружения создаем файл .env:
```
touch .env
```
Для тестирования бота добавляем токен в `.env` файл: `TG_BOT_TOKEN='токен вашего бота'` 

`CHAT_ID='чат ид вашего бота'` можно узнать вызвав https://t.me/userinfobot

Для подключения к платформе Devman посмотрите [api Девмана](https://dvmn.org/api/docs/)

Добавте ваш токен на Девмане в `.env` файл: `DEVMAN_TOKEN='ваш девман токен'`

### 4. Запуск

```
python notification_bot.py
```
### 5. Запуск через Docker
1. Установите [Docker](https://www.docker.com/get-started/)
2. Загружаем в командную строку образ из докерхаба
```pycon
docker pull anikeevmaks/notification_bot:latest
```
3. Запись переменных окружения в командную строку, полученных в 3м шаге:
```pycon
$Env:TG_BOT_TOKEN = '...........'
$Env:DEVMAN_TOKEN = '........'
$Env:CHAT_ID='..........'
```
4. Запуск докер контейнера
```pycon
docker run --rm --name test_ notification_bot -e TG_BOT_TOKEN -e DEVMAN_TOKEN -e CHAT_ID notification_bot
```

Вы должны увидеть результат:

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).