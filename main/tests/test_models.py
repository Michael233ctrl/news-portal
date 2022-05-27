from django.test import TestCase
from main.models import User


class UserTest(TestCase):
    def setUp(self) -> None:
        User.objects.create(username='Mike', email='mike@email.com')
        User.objects.create(username='John', email='john@email.com')

    def test_user_creation(self):
        mike = User.objects.get(username='Mike')
        john = User.objects.get(username='John')
        self.assertTrue(isinstance(mike and john, User))
