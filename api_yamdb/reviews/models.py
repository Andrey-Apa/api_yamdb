from datetime import datetime

from django.db import models
from django.core.validators import MaxValueValidator
from django.conf import settings


CLS_NAME_LEN: int = settings.CLS_NAME_LEN
CURRENT_YEAR: int = int(datetime.now().strftime('%Y'))


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(
        verbose_name='Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='slug-адрес категории',
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name[:CLS_NAME_LEN]


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='slug-адрес жанра',
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name[:CLS_NAME_LEN]


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256,
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=(
            MaxValueValidator(
                CURRENT_YEAR,
                'Год выпуска не должен быть больше текущего.'),
        )
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True, null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name[:CLS_NAME_LEN]

    def display_genre(self):
        """Создает строковое представление жанров для админки."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Жанр'


class GenreTitle(models.Model):
    """Модель для поля many-to-many."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genres',
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Жанр произведений'
        verbose_name_plural = 'Жанры произведений'
        constraints = (
            models.UniqueConstraint(
                fields=('genre', 'title'),
                name='unique_genre_title'),
        )

    def __str__(self) -> str:
        return f'Произведение {self.title} в жанре {self.genre}'
