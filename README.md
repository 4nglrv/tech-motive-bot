# tech-motive-bot
## Python
Python 3.11.6
## Установка
### Создание venv
```bash
python -m venv venv
```

### Подключение к venv
```bash
source venv/bin/activate
```

### Установка зависимостей
```bash
pip install -r requirements.txt
```

## Разработка
### API MODELS Codegen
При изменении API подтягиваем модели из Swagger'a бэка:
```commandline
datamodel-codegen --url http://localhost:3000/api-json --output app/requests/models.py
```

## Переменные окружения
```dotenv
# .env

# ключ для тг бота
TG_BOT_API_KEY=your_tg_bot_api_key

# id пользователей с доступами к боту (через запятую)
USERS_ID=999999999,8888888888
```