from django.urls import reverse
from rest_framework import status

from main.models import Post
from main.tests.test_base import BaseTestCase


class PostApiTestCase(BaseTestCase):
    def test_get(self):
        url = reverse('posts-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_post_by_id(self):
        url = reverse('posts-detail', args=(self.post1.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_posts(self):
        self.assertEqual(2, Post.objects.count())
        url = reverse('posts-list')
        data = {
            "title": "Title",
            "text": "Text",
            "topic": "Topic"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(3, Post.objects.count())

    def test_update_posts(self):
        self.assertEqual('Title of post1', self.post1.title)
        url = reverse('posts-detail', args=(self.post1.pk,))
        data = {"title": "Updated title of post1"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.assertEqual('Updated title of post1', self.post1.title)

    def test_bulk_update_posts(self):
        self.assertEqual('Title of post1', self.post1.title)
        self.assertEqual('Title of post2', self.post2.title)
        url = reverse('posts-list') + "bulk_update/"
        data = [
            {
                "id": 1,
                "title": "Updated title of post1",
                "text": 'Updated text of post1'
            },
            {
                "id": 2,
                "title": "Updated title of post2",
                "text": 'Updated text of post2'
            }
        ]
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.post2.refresh_from_db()
        self.assertEqual('Updated title of post1', self.post1.title)
        self.assertEqual('Updated title of post2', self.post2.title)

    def test_delete_posts(self):
        self.assertEqual(2, Post.objects.count())
        url = reverse('posts-detail', args=(self.post1.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, Post.objects.count())

    def test_like_posts(self):
        url = reverse("posts-detail", args=(self.post1.pk,)) + 'like/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

