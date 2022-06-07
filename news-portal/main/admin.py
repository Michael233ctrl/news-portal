from django.contrib import admin

from .models import User, Post, Company, Like

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Company)
admin.site.register(Like)
