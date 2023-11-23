from django import test


@test.modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})
class IndexViewTestCase(test.TestCase):

    def test_index_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
