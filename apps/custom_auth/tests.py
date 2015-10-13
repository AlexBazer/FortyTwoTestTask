import json

from django.test import TestCase, Client, RequestFactory

from django.contrib.auth.models import User
from custom_auth.models import SipmleRequest
from custom_auth.views import serialize_requests

from pprint import pprint

class TestProfile(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.client = Client()

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
        """
            Send 3 requests and look for then in db
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

    def test_api_last_requests(self):
        """
            Api last requests existence
        """
        response = self.client.get('/api/requests/')
        self.assertEqual(response.status_code, 200)


    def test_serialize_requests(self):
        self.client.get('/')
        request = SipmleRequest.objects.all()[:1]
        manual_serialization = [{
            'timestamp': request[0].timestamp.isoformat(),
            'data': request[0].data,
            'viewed': request[0].viewed
        }]
        self.assertEqual(manual_serialization, serialize_requests(request))

    def test_api_requests_last_10(self):
        """
            Last 10 requests on api
        """
        for i in range(10):
            self.client.get('/')

        last_requests = SipmleRequest.objects.all().order_by('-timestamp')[:10]
        self.assertEqual(
            serialize_requests(last_requests),
            self.client.get('/api/requests/').content
        )
        # response_requests = json.dumps(
        # )
        # for request in last_requests:
        #     self.assertContains(response, request.timestamp.isoformat())

    # def test_requests_is_viewed(self):
    #     """
    #         Mark viewed requests
    #         And check if it exists after second view on /requests/ page
    #     """
    #     self.client.get('/')
    #     last_request_before_view = SipmleRequest.objects.last()

    #     self.client.get('/requests/')
    #     last_requests_after_view = SipmleRequest.objects.get(
    #         pk=last_request_before_view.pk
    #     )
    #     # Check in request was marked ad viewed
    #     self.assertTrue(last_requests_after_view.viewed)

    #     response = self.client.get('/requests/')

    #     # Check if request exists after second view
    #     self.assertNotContains(
    #         response,
    #         last_request_before_view.timestamp.isoformat()
    #     )
