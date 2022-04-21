from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint, CheckConstraint

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

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username']
        constraints = [
            CheckConstraint(
                check=~models.Q(username__iexact="me"),
                name="Can't name user to 'me'"
            ),
            UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user'
            )
        ]

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'


class Title(models.Model):

    def __str__(self):
        return self.title


class Comment(models.Model):

    def __str__(self):
        return self.title


class Post(models.Model):

    def __str__(self):
        return self.title


class Categorie(models.Model):

    def __str__(self):
        return self.title


class Genre(models.Model):

    def __str__(self):
        return self.title
