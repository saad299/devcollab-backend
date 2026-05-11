from .base import *
import dj_database_url
from decouple import config, Csv

DEBUG = False

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv())

CORS_ALLOW_CREDENTIALS = True

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 3600