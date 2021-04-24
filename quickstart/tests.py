from django.test import TestCase
from django.contrib.auth.models import User

from quickstart.models import Follow


class UsersTestCase(TestCase):
    def test_simple(self):
        self.assertEqual(1, 1)

    def test_empty_list_users(self):
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "count": 0,
            "next": None,
            "previous": None,
            "results": [
            ]
        })

    def test_list_users_with_one_user(self):
        User.objects.create(username="Kelly")
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "url": "http://testserver/v1/users/Kelly/",
                    "username": "Kelly",
                    "email": "",
                    "last_name": "",
                    "first_name": ""
                }
            ]
        })

    def test_unknown_url(self):
        response = self.client.get('/incorrect/')
        self.assertEqual(response.status_code, 404)


class FollowTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="John")
        self.user2 = User.objects.create(username="Ann")
        self.user3 = User.objects.create(username="Kelly")
        Follow.objects.create(follower=self.user1, follows=self.user2)

    def test_data_exist(self):
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(Follow.objects.count(), 1)

    def test_new_follow_correct(self):
        self.client.force_login(self.user1)
        response = self.client.post('/v1/follow/John/')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Follow.objects.count(), 2)
