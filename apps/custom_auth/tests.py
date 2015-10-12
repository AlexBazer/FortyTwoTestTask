from django.test import TestCase

from django.contrib.auth.models import User


class TestProfile(TestCase):
    fixtures = ['initial_data.json']

    def test_user_additional_data_exists(self):
        """
            Simple test to check fixtures and additional user data
        """
        user = User.objects.get(pk=1)
        self.assertTrue(user.userprofile)
