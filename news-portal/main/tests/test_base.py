from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import User, Post


def get_token(user):
    return str(RefreshToken.for_user(user).access_token)


class BaseTestCase(APITestCase):
    def setUp(self) -> None:
        self.admin_user = User.objects.create(username='Mike', email='mike@email.com', is_staff=True)
        self.user = User.objects.create(username='John', email='john@email.com')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + get_token(self.admin_user))

        self.post1 = Post.objects.create(title='Title of post1', user_id=self.admin_user, text='Text of post1')
        self.post2 = Post.objects.create(title='Title of post2', user_id=self.user, text='Text of post2')
