from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя.
    Проверяет username на запрещенные значения.
    """
    class Meta:
        model = User
        fields = ('email', 'username')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]

    def validate(self, attrs):
        """Проверка уникальности полей и ввода недопустимого имени 'me'."""
        if attrs['username'] == 'me':
            raise serializers.ValidationError(
                "Поле username не может быть 'me'."
            )
        if attrs['username'] == attrs['email']:
            raise serializers.ValidationError(
                'Поля email и username не должны совпадать.'
            )
        return attrs


class CustomTokenObtainSerializer(serializers.ModelSerializer):
    """Сериализатор формы предоставления данных для аутентификации.
    Валидация по "confirmation_code".
    """
    username_field = User.USERNAME_FIELD
    username = serializers.CharField()
    confirmation_code = serializers.UUIDField()

    class Meta:
        model = User
        fields = ('confirmation_code', 'username', )

    def get_token(self, user):
        """Функция создания токена."""
        refresh = RefreshToken.for_user(user)
        return {'access': str(refresh.access_token), }

    def validate(self, attrs):
        username = attrs['username']
        confirmation_code = attrs['confirmation_code']
        user = get_object_or_404(User, username=username)
        if confirmation_code != user.confirmation_code:
            raise serializers.ValidationError('Ошибка ввода данных')
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения данных пользователя."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "role",
            "first_name",
            "last_name",
            "bio",
        )
