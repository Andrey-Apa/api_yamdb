from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS

from .filters import TitleFilter
from .mixins import ListCreateDeleteViewSet
from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          ReadTitleSerializer, WriteTitleSerializer)
from reviews.models import Category, Genre, Title


class CategoryViewSet(ListCreateDeleteViewSet):
    """Вьюсет для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    """Вьюсет для жанров."""


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_queryset(self):
        return super().get_queryset()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ReadTitleSerializer
        return WriteTitleSerializer
