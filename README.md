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

Для подключения к платформе Devman посмотрите [api Девмана](https://dvmn.org/api/docs/)

Добавте ваш токен на Девмане в `.env` файл: `DEVMAN_TOKEN='ваш девман токен'`

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).