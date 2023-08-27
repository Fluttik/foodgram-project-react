from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from users.validators import validate_username


class User(AbstractUser):
    """Модель пользователя."""
    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимый символ'
        ), validate_username]
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
        blank=False,
        null=False,
        max_length=254,
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return f'{self.username}'


class Follow(models.Model):
    """Модель для подписок."""
    user = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='author',
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
