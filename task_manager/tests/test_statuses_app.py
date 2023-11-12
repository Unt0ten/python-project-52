from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import reverse
from django.core.exceptions import ObjectDoesNotExist

from task_manager.statuses.models import StatusModel


class StatusCodeTestCase(TestCase):

    def setUp(self):
        User.objects.create(username='lion', password='111')
        StatusModel.objects.create(name='Hard work')
        self.user = User.objects.get(username='lion')
        self.status = StatusModel.objects.get(name='Hard work')
        self.status_pk = self.status.id

    def test_statuses_url(self):
        self.client._login(self.user)
        response = self.client.get('/statuses/')
        self.assertEqual(response.status_code, 200)

    def test_statuses_url_anonim(self):
        response = self.client.get(f'/statuses/')
        self.assertRedirects(response, '/login/')

    def test_create_url(self):
        self.client._login(self.user)
        response = self.client.get('/statuses/create/')
        self.assertEqual(response.status_code, 200)

    def test_change_url(self):
        self.client._login(self.user)
        response = self.client.get(f'/statuses/{self.status_pk}/update/')
        self.assertEqual(response.status_code, 200)

    def test_delete_url_auth(self):
        self.client._login(self.user)
        response = self.client.get(f'/statuses/{self.status_pk}/delete/')
        self.assertEqual(response.status_code, 200)


class UsersCUDTestCase(TestCase):

    def setUp(self):
        User.objects.create(username='han', password='111')
        self.user = User.objects.get(username='han')
        self.name_status = {'name': 'Hard work'}
        self.upd_name_status = {'name': 'UltraHard work'}

    def test_create_status_success(self):
        self.client._login(self.user)
        url = reverse('create_status')
        response = self.client.post(url, self.name_status)
        self.assertRedirects(response, '/statuses/')
        find_status = StatusModel.objects.get(name='Hard work')
        self.assertEqual(find_status.name, 'Hard work')

    def test_update_user(self):
        status = StatusModel.objects.create(**self.name_status)
        self.client._login(self.user)
        status_pk = status.id
        url = reverse('update_status', kwargs={'pk': status_pk})
        self.client.post(url, self.upd_name_status)
        update_status = StatusModel.objects.get(id=status_pk)
        self.assertEqual(update_status.name, 'UltraHard work')

    def test_delete_user(self):
        status = StatusModel.objects.create(**self.name_status)
        self.client._login(self.user)
        status_pk = status.id
        url = reverse('delete_status', kwargs={'pk': status_pk})
        self.client.post(url)

        with self.assertRaises(ObjectDoesNotExist):
            StatusModel.objects.get(id=status_pk)
