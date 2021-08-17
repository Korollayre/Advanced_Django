from datetime import datetime

import requests
from django.conf import settings
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from users.models import SocialUser


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = f'https://api.vk.com/method/users.get/?fields=photo_max_orig,bdate,sex,about&access_token={response["access_token"]}&v' \
              f'=5.92 '

    response = requests.get(api_url)

    if response.status_code != 200:
        return

    data = response.json()['response'][0]

    if 'sex' in data:
        if data['sex'] == 1:
            user.socialuser.gender = SocialUser.FEMALE
        elif data['sex'] == 2:
            user.socialuser.gender = SocialUser.MALE

    if 'about' in data:
        user.socialuser.about_me = data['about']

    if 'bdate' in data:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y')
        age = timezone.now().date().year - bdate.year
        if age < 18 or age > 100:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.age = age

    if 'photo_max_orig' in data:
        social_photo = requests.get(data['photo_max_orig'])

        with open(f'{settings.MEDIA_ROOT}/users_images/{user.username}_avatar.jpg', 'wb') as photo:
            photo.write(social_photo.content)

        user.image = f'{settings.MEDIA_ROOT}/users_images/{user.username}_avatar.jpg'

    user.save()
