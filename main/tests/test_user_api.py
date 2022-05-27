from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import User


def get_token(user):
    return str(RefreshToken.for_user(user).access_token)


class UserApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.superuser = User.objects.create(username='Mike', email='mike@email.com', is_superuser=True)
        self.user = User.objects.create(username='John', email='john@email.com')

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + get_token(self.superuser))

    def test_jwt_token(self):
        sign_up_url = reverse("register")
        data = {
            "username": "JohnDoe",
            "email": "JohnDoe@email.com",
            "password": "somePass123",
            "password2": "somePass123"
        }
        response = self.client.post(sign_up_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        sign_in_url = reverse('token_obtain_pair')
        data = {
            "username": "JohnDoe",
            "password": "somePass123",
        }
        response = self.client.post(sign_in_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users(self):
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_by_id(self):
        url = reverse('users-detail', args=(self.superuser.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_users(self):
        self.assertEqual(2, User.objects.count())
        url = reverse('users-list')
        data = {
            "username": "Pieter",
            "email": "p@gmail.com",
            "telephone_number": "12831024"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(3, User.objects.count())

    def test_update_users(self):
        self.assertEqual('Mike', self.superuser.username)
        url = reverse('users-detail', args=(self.superuser.pk,))
        data = {"username": "Michael"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.superuser.refresh_from_db()
        self.assertEqual('Michael', self.superuser.username)

    def test_delete_users(self):
        # self.assertEqual(2, User.objects.count())
        url = reverse('users-detail', args=(self.superuser.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # self.assertEqual(1, User.objects.count())
