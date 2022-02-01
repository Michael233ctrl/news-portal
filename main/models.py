from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPES = [
        (1, 'client'),
        (2, 'admin'),
        (3, 'superuser')
    ]
    email = models.EmailField(unique=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPES, blank=True, null=True)
    company_id = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(blank=True, null=True)
    telephone_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username


class Company(models.Model):
    name = models.CharField(max_length=250, unique=True)
    url = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    logo = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=250)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    text = models.TextField()
    topic = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.title
