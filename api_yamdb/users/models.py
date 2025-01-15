from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from api_yamdb.constants import (
    ADMIN,
    CHOICES,
    MAX_EMAIL_LENGTH,
    MAX_USERNAME_LENGTH,
    MODERATOR,
    USER
)
from users.validators import validate_username


class User(AbstractUser):
    """Абстрактная модель User."""

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=MAX_EMAIL_LENGTH,
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=CHOICES,
        max_length=max([len(field) for field, _ in CHOICES]),
        default=USER,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=MAX_USERNAME_LENGTH,
        unique=True,
        validators=[UnicodeUsernameValidator(), validate_username]
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR
