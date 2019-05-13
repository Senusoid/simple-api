from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework.views import status


class UserTests(APITestCase):

    def test_user_login(self):
        user_data = {
            'username': 'JohnDow1',
            'password': 'qwe1122'
        }
        User.objects.create_user(**user_data)

        url_path = reverse('users:login')
        response = self.client.post(url_path, data=user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_signup(self):
        user_data = {
            'username': 'JohnDow',
            'email': 'jd@email.com',
            'password': 'qwe1122'
        }
        url_path = reverse('users:signup')
        response = self.client.post(url_path, data=user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
