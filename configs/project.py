import os

from dotenv import load_dotenv

load_dotenv()

DJANGO_ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS")
DJANGO_DEBUG = os.getenv("DJANGO_DEBUG")
DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
