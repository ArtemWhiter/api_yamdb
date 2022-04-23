from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint

from api_yamdb.settings import ROLE_CHOICES


class User(AbstractUser):

    email = models.EmailField(
        'Почта',
        max_length=254,
        unique=True
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.CharField(
        'Права пользователя',
        max_length=100,
        choices=ROLE_CHOICES,
        default='user'
    )

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

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    year = models.PositiveSmallIntegerField(db_index=True)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        related_name='title_category',
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1, 'Оценка не может быть меньше 1'),
            MaxValueValidator(10, 'Оценка не может быть выше 10')
        ],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='author_review_title'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text
