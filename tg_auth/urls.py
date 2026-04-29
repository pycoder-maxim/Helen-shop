from django.urls import path
from . import views

app_name = 'tg_auth'

urlpatterns = [
    path('telegram-auth/', views.telegram_auth, name='telegram_auth'),
]
