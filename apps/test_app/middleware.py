import json

from test_app.models import SipmleRequest


class SaveRequestMiddleware(object):
    """
        Collect requests in simple form to db
        Only skip api requests to make in easy for sqlite
    """
    def process_response(self, request, response):
        # Collect request data to the dict
        if '/api/requests/' in request.path:
            # have to remove requests to api
            return response
        request_to_store = {
            'host': request.get_host(),
            'path': request.path,
            'method': request.method,
            'uri': request.build_absolute_uri(),
            'user_agent': request.META.get('HTTP_USER_AGENT', None),
            'remote_addr': request.META.get('REMOTE_ADDR', None),
            'cookies': request.COOKIES,
            'get': request.GET,
            # Have issue with posting
            # # RawPostDataException: You cannot access
            # # body after reading from request's data stream
            # # https://docs.djangoproject.com/en/dev/
            # # # topics/http/middleware/#process-view
            # 'post': request.POST,
            # 'raw_post': request.body,
        }
        SipmleRequest.objects.create(
            data=json.dumps(request_to_store)
        )
        return response
