from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from api_yamdb.constants import (
    MAX_LENGTH_NAME,
    SHORT_TEXT_LENGTH,
    MIN_SCORE_VALUE,
    MAX_SCORE_VALUE
)
from .base import BaseModel
from .validators import validate_year

User = get_user_model()


class Category(BaseModel):

    class Meta(BaseModel.Meta):
        verbose_name = 'Категория',
        verbose_name_plural = 'Категории'


class Genre(BaseModel):

    class Meta(BaseModel.Meta):
        verbose_name = 'Жанр',
        verbose_name_plural = 'Жанры'


class CommentReviewModel(models.Model):
    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:SHORT_TEXT_LENGTH]


class Title(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название'
    )
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        validators=[validate_year]
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение - Жанр'
        verbose_name_plural = 'Произведения - Жанры'

    def __str__(self):
        return f'{self.title} - {self.genre}'


class Review(CommentReviewModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(
                MIN_SCORE_VALUE,
                f'Минимальная оценка {MIN_SCORE_VALUE}'
            ),
            MaxValueValidator(
                MAX_SCORE_VALUE,
                f'Максимальная оценка {MAX_SCORE_VALUE}'
            )
        ]
    )

    class Meta(CommentReviewModel.Meta):
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'
            )
        ]


class Comment(CommentReviewModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta(CommentReviewModel.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
