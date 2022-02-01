from rest_framework import serializers, generics

from .mixins import BulkUpdateSerializerMixin
from .models import User, Post


class UserSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company_id.name')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'telephone_number', 'company')
        read_only_fields = ('id',)


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
    user = serializers.SerializerMethodField()
    id = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'topic', 'text', 'user_id', 'user')
        read_only_fields = ('id', 'user')
        list_serializer_class = BulkUpdateListSerializer

    def get_user(self, obj):
        return [obj.user_id.username, obj.user_id.email]
