# db_config.py

TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["models.pet", "aerich.models"], # Обязательно добавь aerich.models
            "default_connection": "default",
        },
    },
}