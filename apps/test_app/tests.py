from StringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.utils.timezone import now
from test_app.models import CustomUser
from test_app.models import SipmleRequest
from test_app.views import serialize_requests
from test_app.forms import CustomUserForm

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

    def test_index_template_used(self):
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
        self.assertEqual(user, response.context['custom_user'])

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
        self.assertFalse(response.context['custom_user'])


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


class TestEditCustomUser(TestCase):

    def test_form_is_valid_and_data_saved(self):
        """
            Test Form on validnes and data saving
        """
        new_user_data = {
            'first_name': 'Ronam',
            'last_name': 'Romonovich',
            'birthday': '1985-10-05',
            'skype_id': 'rom_rom',
            'jabber_id': 'rom_rom@ya.ya',
            'other_contacts': 'long text',
            'biography': 'another long text',
        }
        imgfile = StringIO(
            'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00'
            '\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
        )
        imgfile.name = 'test_img_file.gif'
        file_dict = {
            'photo': SimpleUploadedFile(
                imgfile.name,
                imgfile.read(),
                content_type='image/gif'
            )
        }

        user = CustomUser.objects.first()
        form = CustomUserForm(
            new_user_data,
            file_dict,
            instance=user)
        form.is_valid()
        self.assertTrue(form.is_valid())
        # save form
        form.save()

        # Test saved data to custom user
        birthday = new_user_data.pop('birthday')
        for key in new_user_data:
            self.assertEqual(new_user_data[key], getattr(user, key))
        # Check user birthday
        self.assertEqual(str(user.birthday), birthday)
        # Check image
        self.assertIn('test_img_file', user.photo.path)

    def test_edit_user_page(self):
        """
            Test edit user page existence
        """
        response = self.client.get('/edit-user/')
        self.assertEqual(response.status_code, 200)

    def test_edit_user_template_used(self):
        """
            Check that edit_user.html template was used in rendering
        """
        response = self.client.get('/edit-user/')
        self.assertTemplateUsed(response, 'test_app/edit_user.html')

    def test_edit_user_context(self):
        """
            Edit user context contain first user from db
        """
        user = CustomUser.objects.first()
        form = CustomUserForm(instance=user)
        response = self.client.get('/edit-user/')

        self.assertEqual(response.context['custom_user'], user)
        self.assertEqual(response.context['form'].instance, form.instance)

    def test_edit_user_page_post(self):
        """
            Test edit user page on data changing
        """
        new_user_data = {
            'first_name': 'Ronam',
            'last_name': 'Romonovich',
            'birthday': '1985-10-05',
            'email': 'some@some.com',
            'skype_id': 'rom_rom',
            'jabber_id': 'rom_rom@ya.ya',
            'other_contacts': 'long text',
            'biography': 'another long text',
        }
        imgfile = StringIO(
            'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00'
            '\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
        )
        imgfile.name = 'test_img_file.gif'
        photo = SimpleUploadedFile(
            imgfile.name,
            imgfile.read(),
            content_type='image/gif'
        )
        new_user_data.update({'photo': photo})
        self.client.post(
            '/edit-user/',
            new_user_data,
        )
        user = CustomUser.objects.first()
        # Test saved data to custom user
        birthday = new_user_data.pop('birthday')
        # Remove photo
        new_user_data.pop('photo')
        for key in new_user_data:
            self.assertEqual(new_user_data[key], getattr(user, key))
        # Check user birthday
        self.assertEqual(str(user.birthday), birthday)
        # Check image
        self.assertIn('test_img_file', user.photo.path)

    def test_edit_user_page_pose_json_error(self):
        """
            After POST with wrong date format view should return error
        """
        new_user_data = {
            'first_name': 'Ronam',
            'last_name': 'Romonovich',
            'birthday': '10-05-1985',
            'email': 'some@some.com',
            'skype_id': 'rom_rom',
            'jabber_id': 'rom_rom@ya.ya',
            'other_contacts': 'long text',
            'biography': 'another long text',
        }
        response = self.client.post(
            '/edit-user/',
            new_user_data,
        )
        form_response = json.loads(response.content)
        self.assertTrue(form_response['errors']['birthday'])
