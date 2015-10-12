import json

from django.test import TestCase, Client

from django.contrib.auth.models import User
from custom_auth.models import SipmleRequest

class TestProfile(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',)

    def test_user_additional_data_exists(self):
        """
            Simple test to check fixtures and additional user data
        """
        user = User.objects.get(pk=1)
        self.assertTrue(user.userprofile)

    def test_index_page(self):
        """
            Test index page existence
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_fields_existence(self):
        """
            Test fields in response content
        """
        user = User.objects.get(pk=1)
        response = self.client.get('/')
        test_fields = [
            'first_name',
            'last_name',
            'email',
        ]
        test_fields_profile = [
            'birthday',
            'jubber_id',
            'skype_id',
            'other_contacts',
        ]
        for field in test_fields:
            content = getattr(user, field)
            if content:
                self.assertContains(response, content)
            else:
                continue
        for field in test_fields_profile:
            content = getattr(user.userprofile, field)
            if content:
                self.assertContains(response, content)
            else:
                continue

    def test_save_reqiest_middware(self):
        response = self.client.get(
            '/',
            {'test_attr': True},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        request = SipmleRequest.objects.last()

        request_from_json = json.loads(request.data)
        self.assetEqual(response.request.meta.get('HTTP_USER_AGENT'), requet_from_json['user_agent'])
