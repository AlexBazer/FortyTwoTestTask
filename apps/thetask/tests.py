from django.core.urlresolvers import resolve
from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase
from django.test.client import RequestFactory
from apps.thetask.views import index


# Create your tests here.
class IndexPageTest(TestCase):
    def setUp(self):
        # set up request factory
        self.factory = RequestFactory()
        self.user = User.objects.create(
            username='test',
            email='test@test.com',
            password='11111'
        )

    def test_resolve_index(self):
        # Simple resolve test
        self.assertEqual(resolve('/'), index)

    def test_auth_user(self):
        # For now auth user will see empty body and title - "Hello <user_name> from theTask" 
        request = self.factory.get('/')
        request.user = self.user()
        response = index(request)
        self.assertInHTML('<title>Hello test from theTask<title>', response.content)

    def test_anonymous_user(self):
        # For anonymous user there will be button register with id="btn-register"
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = index(request)
        self.assertInHTML('<a class="btn btn-primary">Register<a>', response.content)
