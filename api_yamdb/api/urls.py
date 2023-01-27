from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('v1/auth/signup/', views.UserCreateViewSet.as_view()),
    path('v1/auth/token/', views.CustomTokenObtain.as_view()),
    path('v1/', include(router.urls)),
]
