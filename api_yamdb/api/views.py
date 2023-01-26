

from .mixins import ListCreateDeleteViewSet
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer
from reviews.models import Category


class CategoryViewSet(ListCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
