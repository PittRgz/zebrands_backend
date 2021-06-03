import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to create a default user when initializing the app"""

    def handle(self, *args, **options):
        default_admin_user = os.getenv('ADMN_USER')
        default_admin_password = os.getenv('ADMN_PASS')
        default_admin_name = os.getenv('ADMN_NAME')
        # If user does not exists, then create it
        if not get_user_model().objects.filter(email=default_admin_user).exists():
            self.stdout.write('Creating a new User...')
            get_user_model().objects.create_user(
                email=default_admin_user,
                password=default_admin_password,
                name=default_admin_name
            )

        self.stdout.write(f'User {default_admin_user} created!')
