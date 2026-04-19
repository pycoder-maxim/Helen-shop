import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Берем SECRET_KEY из .env
SECRET_KEY = config('SECRET_KEY')

# Берем DEBUG из .env
DEBUG = True

# Берем ALLOWED_HOSTS из .env
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://helen-shop.onrender.com']

# Добавьте все приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Добавлено для allauth
    'shop',
    'cart',
    'orders',
    'accounts',
    # allauth приложения
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.telegram',  # Провайдер Telegram
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Добавлено для allauth
]

ROOT_URLCONF = 'clothing_store.urls'

CART_SESSION_ID = 'cart'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.categories',
                'cart.context_processors.cart',
                'shop.context_processors.wishlist_count',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Для отладки (только для разработки)
INTERNAL_IPS = [
    '127.0.0.1',
]

# Настройки аутентификации
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'login'

# Настройки allauth
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # стандартный бэкенд Django
    'allauth.account.auth_backends.AuthenticationBackend',  # бэкенд allauth
]

# Настройки аккаунтов allauth
ACCOUNT_EMAIL_REQUIRED = False  # Email не обязателен
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Без подтверждения email
ACCOUNT_AUTHENTICATION_METHOD = 'username'  # Авторизация по username
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_LOGOUT_ON_GET = True  # Выход при GET запросе

# Настройки социальной аутентификации
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_STORE_TOKENS = False

# Админка
ADMIN_SITE_HEADER = "HelenShop Администрирование"
ADMIN_SITE_TITLE = "HelenShop"
ADMIN_INDEX_TITLE = "Управление магазином HelenShop"









