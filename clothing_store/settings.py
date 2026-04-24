import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Берем SECRET_KEY из .env
SECRET_KEY = config('SECRET_KEY')

# Берем DEBUG из .env
DEBUG = config('DEBUG', default=False, cast=bool)

# Берем ALLOWED_HOSTS из .env
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://helen-shop.onrender.com', 'http://helen-shop.onrender.com']
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'doodyjkgq',
    'API_KEY': '463822633568354',
    'API_SECRET': 'shSCwQpuEIzqM_1gj3ByMVGbKPY',
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# Добавьте все приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'cloudinary_storage',
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
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← добавь ЭТУ строку ПЕРВОЙ
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
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

# ======================================
# НАСТРОЙКИ СТАТИЧЕСКИХ ФАЙЛОВ
# ======================================
# Это самое важное исправление для админки
STATIC_URL = '/static/'

# Папка, куда будут собираться все статические файлы (CSS, JS) для работы сайта
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Папка, где ты можешь хранить свои собственные CSS/JS файлы (например, для стилей магазина)
STATICFILES_DIRS = [BASE_DIR / 'static']


# Настройки для загружаемых пользователем картинок (медиафайлов)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Для отладки (только для разработки)
INTERNAL_IPS = [
    '127.0.0.1',
]

# Настройки аутентификации
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'login'

# ======================================
# НАСТРОЙКИ ALLAUTH
# ======================================
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Современные настройки allauth, которые уберут предупреждения
# Вместо старых ACCOUNT_EMAIL_REQUIRED, ACCOUNT_USERNAME_REQUIRED и т.д.
ACCOUNT_LOGIN_METHODS = {'username'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGOUT_ON_GET = True

SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_STORE_TOKENS = False


# ======================================
# КАСТОМИЗАЦИЯ АДМИНКИ
# ======================================
ADMIN_SITE_HEADER = "HelenShop Администрирование"
ADMIN_SITE_TITLE = "HelenShop"
ADMIN_INDEX_TITLE = "Управление магазином HelenShop"

# ======================================
# АВТОМАТИЧЕСКОЕ СОЗДАНИЕ TELEGRAM ПРИЛОЖЕНИЯ
# ======================================
try:
    from django.contrib.sites.models import Site
    from allauth.socialaccount.models import SocialApp

    current_site, _ = Site.objects.get_or_create(
        domain='helen-shop.onrender.com',
        defaults={'name': 'HelenShop'}
    )

    telegram_app, created = SocialApp.objects.get_or_create(
        provider='telegram',
        name='Telegram',
        defaults={
            'client_id': '84014347464:AAGxcITa9m8-veQR_wKnKM1koYRTXG0kfA',
        }
    )

    if current_site not in telegram_app.sites.all():
        telegram_app.sites.add(current_site)
        telegram_app.save()

except Exception as e:
    print(f"Telegram app setup error (non-critical): {e}")









