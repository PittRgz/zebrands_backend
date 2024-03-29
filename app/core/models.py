import re

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Model to for customize users model
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Create a new user with ZeBrand email as username

        :param email: str ZeBrand email
        :param password: str Password
        :param extra_fields:
        :return: user
        """
        if not email:
            raise ValueError('User must have an email address')

        # Validating email address
        if not re.match(r'^(\w|\.|\_|\-)+@zebrands.com$', email.lower()):
            raise ValueError('Invalid user. Please enter a valid zebrands email')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)  # Encrypt password
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create a new Super user with ZeBrand email as username

        :param email: str ZeBrand email
        :param password: str Password
        :param extra_fields:
        :return: user
        """
        user = self.create_user(email, password)

        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=225)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # Setting username field as email

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product Model"""
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    brand = models.CharField(max_length=200)
    visits = models.IntegerField(default=0)

    def __str__(self):
        return self.sku
