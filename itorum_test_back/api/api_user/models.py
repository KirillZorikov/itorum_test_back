from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Custom user model """
    username = models.CharField('Имя',
                                max_length=100,
                                unique=True,
                                blank=False,
                                null=False,
                                help_text='Имя пользователя.')
