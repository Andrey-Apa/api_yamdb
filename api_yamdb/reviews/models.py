

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

from users.models import User
CLS_NAME_LEN: int = settings.CLS_NAME_LEN

















































































































class Review(models.Model):
    """Описание модели отзывов на произведения."""
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Оставьте свой отзыв о произведении'
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=(
            MinValueValidator(1, 'Оценка не может быть меньше 1!'),
            MaxValueValidator(10, 'Оценка не может быть больше 10!'),
        ),
        help_text='Укажите вашу оценку в диапазоне от 1 до 10'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review'
            ),
        )

    def __str__(self) -> str:
        return (f'Пользователь {self.author} '
                f'оставил отзыв {self.text[:CLS_NAME_LEN]}')


class Comment(models.Model):
    """Модель комментариев к отзыву."""
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Оставьте свой комментарий к отзыву'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации комментария',
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text[:CLS_NAME_LEN]
