from django.test import TestCase, Client
from django.utils.timezone import now
from apps.test_app.models import CustomUser
from test_app.models import SipmleRequest
from test_app.views import serialize_requests

import json


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

    def test_index_template_user(self):
        """
            Check that index.html template was used in rendering
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'test_app/index.html')

    def test_user_fields_existence_in_index_context(self):
        """
            Test user fields existence in index context
        """
        user = CustomUser.objects.first()
        response = self.client.get('/')
        self.assertEqual(user, response.context['user'])

    def test_user_fields_existence_on_index_html(self):
        """
            Test user fields existence in index html
        """
        user = CustomUser.objects.first()
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

    def test_users_table_is_empty_on_index_context(self):
        """
            If there is no user in CustomUser table context should be empty
        """
        users = CustomUser.objects.all()
        users.delete()
        response = self.client.get('/')
        self.assertFalse(response.context['user'])


class TestRequests(TestCase):
    """
        Test Requests
    """
    def test_save_request_middware_creates(self):
        """
            Send 3 requests and look for them in db
        """
        self.client.get('/')
        self.client.get('/')
        self.client.get('/')
        self.assertEqual(3, SipmleRequest.objects.all().count())

    def test_requests_page(self):
        """
            Requests page existence
        """
        response = self.client.get('/requests/')
        self.assertEqual(response.status_code, 200)

    def test_api_requests_handler(self):
        """
            Api last requests handler existence
        """
        response = self.client.get('/api/requests/')
        self.assertEqual(response.status_code, 200)

    def test_api_requests_handler_method_not_allowed(self):
        """
            Test api requests handler METHOD NOT ALLOWED
        """
        response = self.client.post('/api/requests/')
        self.assertEqual(response.status_code, 405)

    def test_serialize_requests(self):
        """
            Test serialize_requests function
        """
        self.client.get('/')
        request = SipmleRequest.objects.all()[:1]
        manual_serialization = json.dumps([{
            'timestamp': request[0].timestamp.isoformat(),
            'data': request[0].data,
            'viewed': request[0].viewed,
            'id': request[0].pk
        }])
        self.assertEqual(manual_serialization, serialize_requests(request))

    def test_api_requests_get_last_10(self):
        """
            Last 10 requests on api
            if GET parameter timestamp not set
        """
        for i in range(10):
            self.client.get('/')

        last_requests = SipmleRequest.\
            objects.filter(viewed=False).\
            order_by('-timestamp')[:10]
        self.assertEqual(
            serialize_requests(last_requests),
            self.client.get('/api/requests/').content
        )

    def test_api_requests_get_last_added(self):
        """
            Get last added requests after the timestamp
            if GET parameter timestamp is set
        """
        timestamp = now().isoformat()
        for i in range(10):
            self.client.get('/')
            if i == 3:
                timestamp = now().isoformat()

        response = self.client.get(
            '/api/requests/',
            {'timestamp': timestamp}
        )
        self.assertEqual(6, len(json.loads(response.content)))

    def test_api_mark_viewed(self):
        """
            Mark requests with ids was posted
        """
        for i in range(10):
            self.client.get('/')

        last_requests_ids = list(
            SipmleRequest.objects.
            filter(viewed=False).
            order_by('-timestamp').
            values_list('id', flat=True)[:10]
        )

        self.client.post(
            '/api/requests/',
            json.dumps({'viewed_ids': last_requests_ids}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            content_type='application/json',
        )

        last_requests = SipmleRequest.objects.\
            filter(pk__in=last_requests_ids)
        for item in last_requests:
            self.assertTrue(item.viewed)

    def test_api_mark_viewd_nothing_to_mark(self):
        """
            Test api mark viewed requests, in empty list was posted
        """
        response = self.client.post(
            '/api/requests/',
            json.dumps({'viewed_ids': []}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
