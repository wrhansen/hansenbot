import os

os.environ.update(
    {
        "ALLOWED_HOSTS": "localhost",
        "GROUPME_BOT_ID": "",
        "GROUPME_ACCESS_TOKEN": "",
        "GROUPME_OPEN_WEATHER_API_KEY": "",
    }
)


from .settings import *

DATABASES["default"] = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
}

SECRET_KEY = "secret-key"
