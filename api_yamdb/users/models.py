from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import ROLE_CHOICES


class User(AbstractUser):
    username = models.CharField(
        'Пользователь',
        unique=True,
        max_length=150,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        'Почта',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
        null=True
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Права пользователя',
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )
