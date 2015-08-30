from django.core.urlresolvers import resolve
from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase
from django.test.client import RequestFactory
from django.template.loader import render_to_string
from apps.thetask.views import index


# Create your tests here.
class IndexPageTest(TestCase):
    def assert_index(self, user):
        # form request
        request = self.factory.get('/')
        request.user = user
        response = index(request)
        # get rendered template
        template = render_to_string('thetask/index.html', user=user)
        self.assertEqual(template, response.content)

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
        self.assertEqual(resolve('/').func, index)

    def test_auth_user(self):
        # For now auth user will see empty body and title - "Hello <user_name> from theTask" 
        self.assert_index(self.user)

    def test_anonymous_user(self):
        # For anonymous user there will be button register with id="btn-register"
        self.assert_index(AnonymousUser())
