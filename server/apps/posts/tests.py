from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .models import Post, Vote


class PostsTests(APITestCase):
    user_data = {
        'username': 'qwe',
        'password': 'asd',
        'email': 'qwe@qwe.com'
    }

    post_data = {
        'title': 'breakin news',
        'text': 'abrakadabraololol'
    }

    def get_token(self, user_data):
        url_path = reverse('users:login')

        response = self.client.post(url_path, data=user_data, format='json')
        return response.data.get('token')

    def setUp(self):
        self.user = User.objects.create_user(**self.user_data)

    def test_creation_post(self):
        url_path = reverse('posts:posts-list')
        token = self.get_token(self.user_data)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.post(url_path, data=self.post_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post_id = response.data.get('id')
        post = Post.objects.get(id=post_id)
        self.assertEqual(post.user, self.user)

    def test_post_vote(self):
        like = {'value': 1}
        dislike = {'value': -1}

        post = self.user.post_set.create(**self.post_data)
        url_path = reverse('posts:posts-vote', kwargs={"pk": post.id})

        token = self.get_token(self.user_data)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.post(url_path, data=like, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(url_path, data=dislike, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(url_path, data=like, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)