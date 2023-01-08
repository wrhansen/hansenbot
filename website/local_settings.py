import os

from dotenv import load_dotenv

load_dotenv()

from .settings import *

DATABASES["default"] = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
}

SECRET_KEY = "secret-key"
