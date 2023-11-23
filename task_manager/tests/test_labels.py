from django.contrib.auth.models import User
from django import test
from django.shortcuts import reverse
from django.core.exceptions import ObjectDoesNotExist

from task_manager.labels.models import LabelModel


@test.modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})
class StatusCodeTestCase(test.TestCase):

    def setUp(self):
        self.user = User.objects.create(username='Danny', password='111')
        self.label = LabelModel.objects.create(name='Example label')

    def test_labels_url(self):
        self.client._login(self.user)
        response = self.client.get('/labels/')
        self.assertEqual(response.status_code, 200)

    def test_labels_url_anonim(self):
        response = self.client.get('/labels/')
        self.assertRedirects(response, '/login/')

    def test_create_url_anonim(self):
        response = self.client.get('/labels/create/')
        self.assertRedirects(response, '/login/')

    def test_change_url_anonim(self):
        response = self.client.get(f'/labels/{self.label.id}/update/')
        self.assertRedirects(response, '/login/')

    def test_delete_url_anonim(self):
        response = self.client.get(f'/labels/{self.label.id}/delete/')
        self.assertRedirects(response, '/login/')


@test.modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})
class LabelsCUDTestCase(test.TestCase):

    def setUp(self):
        self.user = User.objects.create(username='Han', password='111')
        self.client._login(self.user)
        self.name_label = {'name': 'Hard work'}
        self.upd_name_label = {'name': 'UltraHard work'}

    def test_create_label_success(self):
        url = reverse('create_label')
        response = self.client.post(url, self.name_label)
        self.assertRedirects(response, '/labels/')
        find_label = LabelModel.objects.get(name='Hard work')
        self.assertEqual(find_label.name, 'Hard work')

    def test_update_label(self):
        label = LabelModel.objects.create(**self.name_label)
        url = reverse('update_label', kwargs={'pk': label.id})
        self.client.post(url, self.upd_name_label)
        update_label = LabelModel.objects.get(id=label.id)
        self.assertEqual(update_label.name, 'UltraHard work')

    def test_delete_status(self):
        label = LabelModel.objects.create(**self.name_label)
        url = reverse('delete_label', kwargs={'pk': label.id})
        self.client.post(url)

        with self.assertRaises(ObjectDoesNotExist):
            LabelModel.objects.get(id=label.id)
