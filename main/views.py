from rest_framework.viewsets import ModelViewSet

from .mixins import BulkUpdateRouteMixin
from .models import User, Post
from . import serializers


class UserViewSet(ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class PostViewSet(BulkUpdateRouteMixin):
    serializer_class = serializers.PostSerializer
    queryset = Post.objects.all()
