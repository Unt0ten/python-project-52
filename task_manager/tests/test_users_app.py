from django.test import TestCase, Client
from django.shortcuts import reverse

from task_manager.users.models import CustomUser
from task_manager.users import forms


class StatusCodeTestCase(TestCase):

    def SetUp(self):
        CustomUser.objects.create(username="lion", password="111")
        self.user = CustomUser.objects.last()

    def test_users_url(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_create_url(self):
        response = self.client.get('/users/create/')
        self.assertEqual(response.status_code, 200)

    def test_change_url_auth(self):
        # поправить тесты!
        user_pk = self.user.id
        self.client._login(self.user)
        response = self.client.get(f'/users/{user_pk}/update/')
        self.assertEqual(response.status_code, 200)

    # def test_change_url_anonim(self):
    #     CustomUser.objects.create(username="lion", password="111")
    #     user = CustomUser.objects.last()
    #     user_pk = user.id
    #     self.client._login(user)
    #     response = self.client.get(f'/users/{user_pk}/update/')
    #     self.assertEqual(response.status_code, 200)


class UsersCRUDTestCase(TestCase):

    def SetUp(self):
        self.client = Client()
        self.data = {
            'valid_user': {
                'username': '@user',
                'first_mame': 'Ivan',
                'last_name': 'Ivanov',
                'password1': '111',
                'password2': '111'
            },
            'logged_valid_user': {
                'username': '@user',
                'first_mame': 'Ivan',
                'last_name': 'Ivanov',
                'password1': '111',
                'password2': '111',
                'is_authenticated': 'True'
            },
            'wrong_user_username': {
                'username': '$user',
                'first_mame': 'Ivan',
                'last_name': 'Ivanov',
                'password1': '111',
                'password2': '111'
            },
            'wrong_user_password': {
                'username': '@user',
                'first_mame': 'Ivan',
                'last_name': 'Ivanov',
                'password1': '111',
                'password2': '112'
            },
            'anonimus_user': {
                'username': '',
                'first_mame': '',
                'last_name': '',
                'password1': '',
                'password2': '',
                'is_anonymous': 'True',
            },
        }

    def test_users_view(self):
        pass

