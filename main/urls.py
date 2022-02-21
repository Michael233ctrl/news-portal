from rest_framework import routers
from django.urls import path, include

from main import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'posts', views.PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls))
]
