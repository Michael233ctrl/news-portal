from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .mixins import BulkUpdateRouteMixin
from .models import User, Post, Company, Like
from . import serializers
from .permissions import IsOwner, IsAuthorOrReadOnly, IsAdminUserOrReadOnly


class RegUserView(CreateAPIView):
    serializer_class = serializers.CreateUserSerializer
    permission_classes = (AllowAny,)


class UserViewSet(ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.filter(is_active=True).select_related('company_id')
    permission_classes = (IsOwner,)

    def get_permissions(self):
        if self.action in ['list', 'create']:
            self.permission_classes = (IsAdminUser,)
        return super(UserViewSet, self).get_permissions()

    def perform_destroy(self, instance):
        if self.request.user.is_superuser:
            super(UserViewSet, self).perform_destroy(instance)
            return
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

    @action(detail=True, methods=['get'], permission_classes=(IsAuthenticated,))
    def like(self, request, pk=None):
        post = self.get_object()
        option = "like"
        if Like.objects.filter(post=post, user=request.user):
            option = "unlike"
            post.set_reaction(request.user, option)
            return Response({'message': "unlike"}, status=status.HTTP_200_OK)
        try:
            post.set_reaction(request.user, option)
        except ValueError as e:
            return Response({'message': f'{e}'}, status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(post)
        return Response(serializer.data)


class CompanyViewSet(ModelViewSet):
    serializer_class = serializers.CompanySerializer
    queryset = Company.objects.all().prefetch_related('users')
    permission_classes = (IsAdminUserOrReadOnly,)
