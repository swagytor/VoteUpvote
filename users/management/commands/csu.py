from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.create_superuser(
            username='admin',
            first_name='IT',
            last_name='Power',
            password='12345'
        )
