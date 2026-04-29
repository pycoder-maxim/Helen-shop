import hashlib
import hmac
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect

BOT_TOKEN = '84014347464:AAGxcITa9m8-veQR_wKnKM1koYRTXG0kfA'


def telegram_auth(request):
    data = request.GET.dict()

    if 'hash' not in data:
        return redirect('/?error=no_hash')

    hash_string = data.pop('hash')
    sorted_keys = sorted(data.keys())
    check_string = '\n'.join([f'{k}={data[k]}' for k in sorted_keys])
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    computed_hash = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()

    if computed_hash == hash_string:
        telegram_id = data.get('id')
        unique_username = f'tg_{telegram_id}'
        user, created = User.objects.get_or_create(
            username=unique_username,
            defaults={
                'first_name': data.get('first_name', ''),
                'last_name': data.get('last_name', ''),
                'email': f'{telegram_id}@telegram.user',
            }
        )
        login(request, user)
        return redirect('/')
    else:
        return redirect('/?error=invalid_hash')
