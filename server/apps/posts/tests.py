from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .models import Post, Vote


class BaseViewTest(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = User.objects.create(username='qwe', password='asd', email='qwe@qwe.com')
        self.post_data = {
            'title': 'breakin news',
            'text': 'abrakadabraololol',
            'user': self.user.id
        }


class PostCreationTest(BaseViewTest):

    def test_creation_post(self):
        response = self.client.post('posts', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


