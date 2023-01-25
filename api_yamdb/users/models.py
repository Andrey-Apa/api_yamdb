from django.contrib.auth.models import AbstractUser

from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    bio = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True
    )

    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=25,
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=30,
        choices=ROLES,
        default=USER
    )

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_login_fields',

            ),
        )
