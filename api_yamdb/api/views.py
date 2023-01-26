from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Review, Title

from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorAdminModeratorOrReadOnly)

from .serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для Отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)
    
    def get_title(self):
        """Получение произведения по id."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title
    
    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title())

    def get_queryset(self):
        queryset = self.get_title().reviews.all()
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для Комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)

    def get_review(self):
        """Получение отзыва по id."""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review())

    def get_queryset(self):
        queryset = self.get_review().comments.all()
        return queryset
