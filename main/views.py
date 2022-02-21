from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .mixins import BulkUpdateRouteMixin
from .models import User, Post
from . import serializers


class UserViewSet(ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class PostViewSet(BulkUpdateRouteMixin, ModelViewSet):
    serializer_class = serializers.PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['title', 'text', 'topic']
    search_fields = ['title']
