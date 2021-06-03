import os

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTRests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for DB when DB is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as connection_handler:
            connection_handler.return_value = True
            call_command('wait_for_db')

            # Check if our call command is called only once
            self.assertEqual(connection_handler.call_count, 1)

    # Mocking time.sleep in order to skip waiting time
    @patch('time.sleep', return_value=True)
    def test_wait_for_db_not_ready(self, time_sleep):
        """Test waiting for DB"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as connection_handler:
            # Raise OperationalError 5 times and the sixth return True
            connection_handler.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')

            # Check if our call command is called 6 times
            self.assertEqual(connection_handler.call_count, 6)

    def test_create_default_user_success(self):
        """Test that admin@zebrands.com user is created"""
        call_command('create_user')

        # check that the admin user exists
        self.assertTrue(get_user_model().objects.filter(email=os.getenv('ADMN_USER')).exists())
