from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.core.exceptions import ObjectDoesNotExist
from django import test

from task_manager.tasks.models import TaskModel
from task_manager.statuses.models import StatusModel
from task_manager.labels.models import LabelModel


@test.modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})
class TasksCodeTestCase(test.TestCase):

    def setUp(self):
        self.user = User.objects.create(username='lion', password='111')
        self.status = StatusModel.objects.create(name='status')
        # self.labels = LabelModel.objects.create(name='labels')
        self.user_pk = self.user.id
        self.task = TaskModel.objects.create(
            name='task',
            description='about task',
            status=self.status,
            author=self.user,
            # labels=self.labels,
        )

    def test_tasks_url(self):
        self.client._login(self.user)
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)

    def test_tasks_url_anonim(self):
        response = self.client.get('/tasks/')
        self.assertRedirects(response, '/login/')

    def test_task_view_url(self):
        self.client._login(self.user)
        response = self.client.get(f'/tasks/{self.task.id}/update/')
        self.assertEqual(response.status_code, 200)

    def test_task_view_url_anonim(self):
        response = self.client.get(f'/tasks/{self.task.id}/update/')
        self.assertRedirects(response, '/login/')

    def test_create_url(self):
        self.client._login(self.user)
        response = self.client.get('/tasks/create/')
        self.assertEqual(response.status_code, 200)

    def test_create_url_anonim(self):
        response = self.client.get('/tasks/create/')
        self.assertRedirects(response, '/login/')

    def test_change_url_anonim(self):
        response = self.client.get(f'/tasks/{self.task.id}/update/')
        self.assertRedirects(response, '/login/')

    def test_delete_url_anonim(self):
        response = self.client.get(f'/tasks/{self.task.id}/delete/')
        self.assertRedirects(response, '/login/')

    def test_permissions_url_delete(self):
        user = User.objects.create(username='Bob', password='111')
        self.client._login(user)
        response = self.client.get(f'/tasks/{self.task.id}/delete/')
        self.assertRedirects(response, '/tasks/')


@test.modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})
class TasksCUDTestCase(test.TestCase):

    @classmethod
    def setUpTestData(cls):
        author_data = {
            'username': '@user',
            'first_name': 'Sven',
            'last_name': 'Pavlov',
            'password': '111',
        }
        executor_data = {
            'username': 'vanishe',
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'password': '111',
        }
        cls.author = User.objects.create(**author_data)
        cls.executor = User.objects.create(**executor_data)
        cls.status = StatusModel.objects.create(name='status')
        # cls.labels = LabelModel.objects.create(name='labels')
        # cls.labels_upd = LabelModel.objects.create(name='updated labels')
        cls.status_upd = StatusModel.objects.create(name='updated status')

        cls.task_fields = {
            'name': 'Task',
            'description': 'This is task',
            'status': cls.status.pk,
            # 'labels': cls.labels.pk,
            'executor': cls.author.pk,
        }
        cls.task_fields_upd = {
            'name': 'Task upd',
            'description': 'This is task upd',
            'status': cls.status_upd.pk,
            # 'labels': cls.labels_upd.pk,
            'executor': cls.executor.pk,
        }
        cls.task_data1 = {
            'name': 'Task',
            'description': 'This is task',
            'status': cls.status,
            # 'labels': cls.labels.pk,
            'executor': cls.author,
            'author': cls.author
        }
        cls.task_data2 = {
            'name': 'Task',
            'description': 'This is task',
            'status': cls.status,
            # 'labels': cls.labels.pk,
            'executor': cls.author,
            'author': cls.executor
        }

    def setUp(self):
        self.client._login(self.author)

    def test_create_task_success(self):
        url = reverse('create_task')
        response = self.client.post(url, self.task_fields)
        self.assertRedirects(response, '/tasks/')
        find_task = TaskModel.objects.get(name='Task')
        self.assertEqual(find_task.name, 'Task')

    def test_update_task(self):
        origin_task = TaskModel.objects.create(**self.task_data1)
        url = reverse('update_task', kwargs={'pk': origin_task.id})
        response = self.client.post(url, self.task_fields_upd)
        self.assertRedirects(response, '/tasks/')
        updated_task = TaskModel.objects.get(id=origin_task.id)
        self.assertEqual(updated_task.name, 'Task upd')

    def test_delete_task(self):
        task = TaskModel.objects.create(**self.task_data1)
        url = reverse('delete_task', kwargs={'pk': task.id})
        self.client.post(url)

        with self.assertRaises(ObjectDoesNotExist):
            TaskModel.objects.get(id=task.id)

    def test_delete_task_without_access(self):
        task = TaskModel.objects.create(**self.task_data2)
        response = self.client.get(f'/tasks/{task.id}/delete/')

        self.assertRedirects(response, '/tasks/')


@test.modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})
class FilterTasksTestCase(test.TestCase):

    @classmethod
    def setUpTestData(cls):
        author_data = {
            'username': 'user',
            'first_name': 'Sven',
            'last_name': 'Pavlov',
            'password': '111',
        }
        executor_data = {
            'username': 'vanishe',
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'password': '111',
        }
        cls.author = User.objects.create(**author_data)
        cls.executor = User.objects.create(**executor_data)
        cls.status1 = StatusModel.objects.create(name='status1')
        cls.status2 = StatusModel.objects.create(name='status2')
        cls.label1 = LabelModel.objects.create(name='labels')
        cls.label2 = LabelModel.objects.create(name='updated labels')

        cls.task1_data = {
            'name': 'Task1',
            'description': 'This is task1',
            'status': cls.status1,
            'executor': cls.author,
            'author': cls.author
        }
        cls.task2_data = {
            'name': 'Task2',
            'description': 'This is task2',
            'status': cls.status2,
            'executor': cls.executor,
            'author': cls.author
        }
        cls.task3_data = {
            'name': 'Task3',
            'description': 'This is task3',
            'status': cls.status1,
            'executor': cls.author,
            'author': cls.author
        }
        cls.task4_data = {
            'name': 'Task4',
            'description': 'This is task4',
            'status': cls.status2,
            'executor': cls.author,
            'author': cls.executor
        }
        cls.task1 = TaskModel.objects.create(**cls.task1_data)
        cls.task1.labels.add(cls.label1)
        cls.task2 = TaskModel.objects.create(**cls.task2_data)
        cls.task2.labels.add(cls.label1)
        cls.task3 = TaskModel.objects.create(**cls.task3_data)
        cls.task3.labels.add(cls.label2)
        cls.task4 = TaskModel.objects.create(**cls.task4_data)
        cls.task4.labels.add(cls.label2)

    def setUp(self):
        self.client._login(self.author)

    def test_filter_tasks_status(self):
        url = f'/tasks/?status={self.status1.id}&executor=&labels='
        response = self.client.get(url)
        count_records = len(response.context['object_list'].qs)
        self.assertEqual(count_records, 2)

    def test_filter_tasks_executor(self):
        url = f'/tasks/?status=&executor={self.executor.id}&labels='
        response = self.client.get(url)
        count_records = len(response.context['object_list'].qs)
        self.assertEqual(count_records, 1)

    def test_filter_tasks_author(self):
        url = '/tasks/?status=&executor=&labels=&author=on'
        response = self.client.get(url)
        count_records = len(response.context['object_list'].qs)
        self.assertEqual(count_records, 3)

    def test_filter_tasks_label(self):
        url = f'/tasks/?status=&executor=&labels={self.label1.id}'
        response = self.client.get(url)
        count_records = len(response.context['object_list'].qs)
        self.assertEqual(count_records, 2)

    def test_filter_tasks_all(self):
        url = f'/tasks/?status={self.status2.id}&executor={self.executor.id}' \
              f'&labels={self.label1.id}&author=on'
        response = self.client.get(url)
        count_records = len(response.context['object_list'].qs)
        self.assertEqual(count_records, 1)
