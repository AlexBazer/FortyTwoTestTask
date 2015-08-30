from django.core.urlresolvers import resolve
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory, Client
from apps.thetask.views import index


# Create your tests here.
class IndexPageTest(TestCase):
    def setUp(self):
        # set up request factory
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(
            username='test',
            email='test@test.com',
            password='11111'
        )

    def test_resolve_index(self):
        # Simple resolve test
        self.assertEqual(resolve('/').func, index)

    def test_auth_user(self):
        # For now auth user request content will content username
        self.client.login(username='test', password='11111')
        response = self.client.get('/')
        self.assertContains(response, self.user.username)
        self.client.logout()

    def test_anonymous_user(self):
        response = self.client.get('/')
        # For anonymous user request content will content Register word
        self.assertContains(response, 'Register')
