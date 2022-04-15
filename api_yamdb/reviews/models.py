from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.title

class Title(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    year = models.IntegerField()
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='title_genre',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='title_category',
    )
    
    def __str__(self):
        return self.title


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews', blank=True, null=True)
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    score = models.IntegerField(
        'Оценка',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ],
    )

    def __str__(self):
        return self.text


class Comment(models.Model):

    def __str__(self):
        return self.title