from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User, Post, Company
from .mixins import BulkUpdateSerializerMixin


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=User.CLIENT,
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company_id', read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'telephone_number', 'company')


class BulkUpdateListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        post_mapping = {post.id: post for post in instance}
        data_mapping = {item['id']: item for item in validated_data}

        ret = []
        for post_id, data in data_mapping.items():
            post = post_mapping.get(post_id, None)
            if post is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(post, data))

        for post_id, post in post_mapping.items():
            if post_id not in data_mapping:
                post.delete()

        return ret


class PostSerializer(BulkUpdateSerializerMixin, serializers.ModelSerializer):
    username = serializers.CharField(source='user_id', read_only=True)
    user_company = serializers.CharField(source='user_id.company_id', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'topic', 'text', 'username', 'user_company')
        list_serializer_class = BulkUpdateListSerializer


class CompanySerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ('name', 'url', 'users')
