from django.core.urlresolvers import resolve
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from apps.thetask.views import index


# Create your tests here.
class IndexPageTest(TestCase):
    def setUp(self):
        """
            Get client and create user
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username='test',
            email='test@test.com',
            password='11111'
        )

    def test_resolve_index(self):
        """
            Simple resolve test
        """
        self.assertEqual(resolve('/').func, index)

    def test_auth_user(self):
        """
            For now auth user request content will content username
        """
        self.client.login(username='test', password='11111')
        response = self.client.get('/')
        self.assertContains(response, self.user.username)
        self.client.logout()

    def test_anonymous_user(self):
        """
            For anonymous user request content will content Register word
        """
        response = self.client.get('/')
        self.assertContains(response, 'Register')
