import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until DB is available"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for Database...')   # Output a message to the screen
        db_conn = None

        # Wait until DB is available, try every second
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database is available'))
