from django.test import TestCase, Client

from apps.test_app.models import CustomUser


class TestProfile(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.client = Client()

    def test_index_page(self):
        """
            Test index page existence
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_template_userf(self):
        """
            Check that index.html template was used in rendering 
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'test_app/index.html')

    def test_fields_existence(self):
        """
            Test fields text existence in response content
        """
        user = CustomUser.objects.get(pk=1)
        response = self.client.get('/')
        # Fields to check
        test_fields = [
            'first_name',
            'last_name',
            'email',
            'birthday',
            'jabber_id',
            'skype_id',
            'other_contacts',
        ]

        for field in test_fields:
            # Get field value from model and check it in response context
            content = getattr(user, field)
            if content:
                self.assertContains(response, content)
            else:
                continue
