from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet

v1_router = DefaultRouter()
v1_router.register('category', CategoryViewSet, basename='category')
v1_router.register('genre', GenreViewSet, basename='genre')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
