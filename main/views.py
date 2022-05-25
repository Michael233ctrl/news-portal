from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .mixins import BulkUpdateRouteMixin
from .models import User, Post, Company
from . import serializers
from .permissions import IsOwner, IsAuthorOrReadOnly, IsAdminUserOrReadOnly


class RegUserView(CreateAPIView):
    serializer_class = serializers.CreateUserSerializer
    permission_classes = (AllowAny,)


class UserViewSet(ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.select_related('company_id')
    permission_classes = (IsOwner,)

    def get_permissions(self):
        if self.action in ['list', 'create']:
            self.permission_classes = (IsAdminUser,)
        return super(UserViewSet, self).get_permissions()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class PostViewSet(BulkUpdateRouteMixin, ModelViewSet):
    serializer_class = serializers.PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['title', 'text', 'topic']

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.select_related('user_id__company_id')
        company = self.request.query_params.get('company', None)
        if company:
            queryset = Post.objects.filter(user_id__company_id__name=company)

        return queryset


class CompanyViewSet(ModelViewSet):
    serializer_class = serializers.CompanySerializer
    queryset = Company.objects.all().prefetch_related('users')
    permission_classes = (IsAdminUserOrReadOnly,)
