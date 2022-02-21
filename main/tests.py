from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Company


class PostApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.companies = []
        for i in range(10000):
            self.companies.append(Company.objects.create(name=str(i)))

    def test_update_company(self):
        url = reverse('company_update')

