import rest_framework.permissions as rest_permissions
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import (
    filters,
    generics,
    response,
    status,
    viewsets
)
from rest_framework.decorators import action
from users.models import User

from . import permissions, serializers


class UserCreateViewSet(generics.CreateAPIView):
    """Класс для создания пользователя.
    """
    permission_classes = (rest_permissions.AllowAny,)
    serializer_class = serializers.UserCreateSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = serializers.UserCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(
            User,
            username=serializer.data['username']
        )
        mail_subject = 'Добро пожаловать на YaMDB :)'
        send_mail(
            mail_subject,
            f'Приветствуем {user.username}!'
            f'''ваш confirmation_code для получения API токена:
            {user.confirmation_code}''',
            settings.POST_EMAIL,
            [f'{user.email}'],

        )

        return response.Response(
            data={
                'email': serializer.data['email'],
                'username': serializer.data['username']
            },
            status=status.HTTP_200_OK
        )


class CustomTokenObtain(generics.CreateAPIView):
    """Класс для создания JWT токена.
    """
    permission_classes = (rest_permissions.AllowAny,)
    serializer_class = serializers.CustomTokenObtainSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = serializers.CustomTokenObtainSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.data['username']
        )

        token = serializer.get_token(user)

        return response.Response(
            {'token': f"{ token['access'] }"},
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет Пользователя.
    Реализованы методы чтения, создания,
    частичного обновления и удаления объектов.
    Есть поиск по полю username.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AdminOnly,)
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)

    @action(
        detail=False,
        methods=["get", "patch"],
        url_path="me",
        url_name="me",
        serializer_class=serializers.UserSerializer,
        permission_classes=(
            rest_permissions.IsAuthenticated,
        ),
    )
    def me(self, request):
        """Доступ пользователя к своей учетной записи по '/users/me/'."""
        me_user = request.user
        serializer = self.get_serializer(me_user)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                me_user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(email=me_user.email, role=me_user.role)
            return response.Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return response.Response(serializer.data, status=status.HTTP_200_OK)
