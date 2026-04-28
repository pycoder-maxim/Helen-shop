import os
import django

# Настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_store.settings')
django.setup()

from allauth.socialaccount.models import SocialApp

# Удаляем все Social App с provider='telegram'
deleted, _ = SocialApp.objects.filter(provider='telegram').delete()
print(f"Удалено {deleted} записей Telegram")

# Показываем оставшиеся записи
remaining = SocialApp.objects.filter(provider='telegram')
print(f"Осталось записей: {remaining.count()}")
