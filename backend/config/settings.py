from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-typography-dev-key-change-in-prod')

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

BITRIX_STUB_DIR = BASE_DIR / 'data' / 'bitrix_stub'

_bitrix_webhook = os.getenv('BITRIX_WEBHOOK_URL', '').strip()
BITRIX_WEBHOOK_URL = _bitrix_webhook
# true, если в .env указан URL и BITRIX_ENABLED не выключен явно
BITRIX_ENABLED = os.getenv('BITRIX_ENABLED', 'true' if _bitrix_webhook else 'false').lower() in (
    '1',
    'true',
    'yes',
)
# При ошибке Bitrix — дополнительно писать JSON в data/bitrix_stub/
BITRIX_STUB_FALLBACK = os.getenv('BITRIX_STUB_FALLBACK', 'true').lower() in ('1', 'true', 'yes')
# deal — заявки в CRM → Сделки; lead — CRM → Лиды
BITRIX_CRM_ENTITY = os.getenv('BITRIX_CRM_ENTITY', 'deal').strip().lower()
# ID воронки сделок (0 = «Общая воронка»), обычно можно не указывать
_deal_cat = os.getenv('BITRIX_DEAL_CATEGORY_ID', '').strip()
BITRIX_DEAL_CATEGORY_ID = int(_deal_cat) if _deal_cat.isdigit() else None

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'typography_db',
        'USER': 'postgres',
        'PASSWORD': 'Pass123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Novosibirsk'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Публичный URL сайта (API, media, staff). В dev: http://127.0.0.1:8000
SITE_BASE_URL = os.getenv('SITE_BASE_URL', 'http://127.0.0.1:8000').rstrip('/')
# Раздавать собранный Vue с Django (не нужен отдельный Vite для ссылок из CRM)
SERVE_FRONTEND_FROM_DJANGO = os.getenv('SERVE_FRONTEND_FROM_DJANGO', 'true').lower() in (
    '1',
    'true',
    'yes',
)
# CRM-ссылки на /staff/quotes/… — по умолчанию тот же хост, что и API
FRONTEND_BASE_URL = os.getenv(
    'FRONTEND_BASE_URL',
    SITE_BASE_URL if SERVE_FRONTEND_FROM_DJANGO else 'http://127.0.0.1:5173',
).rstrip('/')

QUOTE_MAX_ATTACHMENTS = 3
QUOTE_MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 МБ на файл

FILE_UPLOAD_MAX_MEMORY_SIZE = 30 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 35 * 1024 * 1024

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Почта: анкета «Отправить резюме»
RESUME_NOTIFY_EMAIL = os.getenv('RESUME_NOTIFY_EMAIL', 'lina.verxoglyadova@gmail.com').strip()

EMAIL_HOST = os.getenv('EMAIL_HOST', '').strip()
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'true').lower() in ('1', 'true', 'yes')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '').strip()
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '').strip()
DEFAULT_FROM_EMAIL = os.getenv(
    'DEFAULT_FROM_EMAIL',
    EMAIL_HOST_USER or 'noreply@typography.local',
).strip()

RESUME_EMAIL_USE_SMTP = bool(EMAIL_HOST and EMAIL_HOST_USER and EMAIL_HOST_PASSWORD)

if RESUME_EMAIL_USE_SMTP:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    # Без SMTP: письма в папку data/resume_outbox (для локальной проверки)
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = BASE_DIR / 'data' / 'resume_outbox'
    EMAIL_FILE_PATH.mkdir(parents=True, exist_ok=True)

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]

CORS_ALLOW_CREDENTIALS = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}
