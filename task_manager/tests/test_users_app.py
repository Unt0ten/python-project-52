from django.test import TestCase
from django.shortcuts import reverse
from django.core.exceptions import ObjectDoesNotExist

from task_manager.users.models import CustomUser


class StatusCodeTestCase(TestCase):

    def setUp(self):
        CustomUser.objects.create(username='lion', password='111')
        CustomUser.objects.create(username='user', password='123')
        self.logged_user = CustomUser.objects.get(username='lion')
        self.anonim_user = CustomUser.objects.get(username='user')
        self.anonim_user_pk = self.anonim_user.id
        self.logged_user_pk = self.logged_user.id

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
        self.client._login(self.logged_user)
        response = self.client.get(f'/users/{self.logged_user_pk}/update/')
        self.assertEqual(response.status_code, 200)

    def test_change_url_anonim(self):
        response = self.client.get(f'/users/{self.logged_user_pk}/update/')
        self.assertRedirects(response, '/login/')

    def test_delete_url_auth(self):
        self.client._login(self.logged_user)
        response = self.client.get(f'/users/{self.logged_user_pk}/delete/')
        self.assertEqual(response.status_code, 200)

    def test_delete_url_anonim(self):
        response = self.client.get(f'/users/{self.anonim_user_pk}/delete/')
        self.assertRedirects(response, '/login/')

    def test_permissions_url_change(self):
        self.client._login(self.logged_user)
        response = self.client.get(f'/users/{self.anonim_user_pk}/update/')
        self.assertRedirects(response, '/users/')

    def test_permissions_url_delete(self):
        self.client._login(self.logged_user)
        response = self.client.get(f'/users/{self.anonim_user_pk}/delete/')
        self.assertRedirects(response, '/users/')


class UsersCUDTestCase(TestCase):

    def setUp(self):
        self.data = {
            'valid_user': {
                'username': '@user',
                'first_mame': 'Ivan',
                'last_name': 'Ivanov',
                'password1': '111',
                'password2': '111'
            },
            'updated_valid_user': {
                'username': '@master',
                'first_mame': 'iVAN',
                'last_name': 'Ivanoff',
                'password1': '123',
                'password2': '123',
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
        }

        self.user_data = {
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'username': 'vanishe',
            'password': '111',
            }

    def test_create_user_success(self):
        url = reverse('create_user')
        user = self.data['valid_user']
        response = self.client.post(url, user)
        self.assertRedirects(response, '/login/')
        find_user = CustomUser.objects.get(username='@user')
        self.assertEqual(find_user.username, '@user')

    def test_create_user_false_username(self):
        url = reverse('create_user')
        wrong_user_username = self.data['wrong_user_username']
        self.client.post(url, wrong_user_username)

        with self.assertRaises(ObjectDoesNotExist):
            CustomUser.objects.get(username='$user')

    def test_create_user_false_password(self):
        url = reverse('create_user')
        wrong_user_password = self.data['wrong_user_password']
        self.client.post(url, wrong_user_password)

        with self.assertRaises(ObjectDoesNotExist):
            CustomUser.objects.get(username='@user')

    def test_update_user(self):
        user = CustomUser.objects.create(**self.user_data)
        self.client._login(user)
        user_pk = user.id
        url = reverse('update_user', kwargs={'pk': user_pk})
        self.client.post(url, self.data['updated_valid_user'])
        update_user = CustomUser.objects.get(id=user_pk)
        self.assertEqual(update_user.username, '@master')

    def test_delete_user(self):
        user = CustomUser.objects.create(**self.user_data)
        self.client._login(user)
        user_pk = user.id
        url = reverse('delete_user', kwargs={'pk': user_pk})
        self.client.post(url)

        with self.assertRaises(ObjectDoesNotExist):
            CustomUser.objects.get(id=user_pk)



