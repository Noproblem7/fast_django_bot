``` project_root/
│
├── backend/
│   ├── fastapi_app/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── config.py
│   │   │   ├── routers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── api_v1.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   ├── alembic.ini
│   └── manage.py
│
├── web_app/
│   ├── django_app/
│   │   ├── manage.py
│   │   ├── django_app/
│   │   │   ├── __init__.py
│   │   │   ├── settings.py
│   │   │   ├── urls.py
│   │   │   ├── wsgi.py
│   │   │   ├── asgi.py
│   │   │   ├── templates/
│   │   │   ├── static/
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│
├── telegram_bot/
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── bot.py
│   │   ├── config.py
│   │   ├── handlers/
│   │   │   ├── __init__.py
│   │   │   ├── start.py
│   │   │   ├── echo.py
│   ├── requirements.txt
│   ├── Dockerfile
│
├── .env
├── docker-compose.yml
└── README.md
```