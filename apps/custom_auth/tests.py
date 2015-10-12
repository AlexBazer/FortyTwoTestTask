from django.test import TestCase

class TestProfile(TestCase):
    fixtures = ['initial_data.json']

    def test_user_data(self):
        pass