from django.core.management import BaseCommand

from users.models import User, SocialUser


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            SocialUser.objects.create(user=user)
