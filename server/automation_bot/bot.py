import os
import random
import string

import requests

from automation_bot import config_file


class ContentGenerator:
    email_domain = '@email.com'

    def _generate_word(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def generate_user_data(self):
        return {
            "username": self._generate_word(10),
            "email": f'{self._generate_word(10)}{self.email_domain}',
            "password": self._generate_word(10),
        }

    def generate_post_data(self):
        return {
            "title": self._generate_word(10),
            "text": self._generate_word(100),
        }


class SimpleApi:
    endpoint = config_file.ENDPOINT
    token = None

    def _request(self, path, data=None):
        url = f'{self.endpoint}{path}'
        headers = {'Authorization': f'Bearer {self.token}' if self.token else None}
        if data:
            response = requests.post(url=url, json=data, headers=headers)
        else:
            response = requests.get(url=url, headers=headers)

        if response.status_code not in [200, 201]:
            import pdb; pdb.set_trace()
            print(response.text)

        return response

    def signin(self, user_data):
        path = 'api/user/auth'
        res = self._request(path, data=user_data)
        token = res.json()['token']
        self.token = token

    def signup(self, user_data):
        path = 'api/user/create'
        self._request(path, data=user_data)

        self.signin(user_data)

    def create_post(self, post_data):
        path = 'api/posts/'
        res = self._request(path, data=post_data)

    def post_like(self, pk=None):
        if pk is None:
            pk = Post.objects.order_by('?').first().id
        data = {'value': 1}

        path = f'api/posts/{pk}/vote/'
        res = self._request(path, data=data)




def main():
    data_gen = ContentGenerator()

    for i in range(config_file.number_of_users+1):
        print(i)
        api = SimpleApi()

        user_data = data_gen.generate_user_data()
        api.signup(user_data)

        for i in range(config_file.max_posts_per_user+1):
            post_data = data_gen.generate_post_data()
            api.create_post(post_data)

        for i in range(config_file.max_like_per_user+1):
            api.post_like()


if __name__ == '__main__':
    # print(os.getenv("DJANGO_SETTINGS_MODULE"))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    import django
    django.setup()
    from apps.posts.models import Post

    main()