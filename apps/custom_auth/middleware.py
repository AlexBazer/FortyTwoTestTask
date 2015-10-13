import json

from custom_auth.models import SipmleRequest


class SaveRequestMiddleware(object):
    def process_response(self, request, response):
        # Collect request data to the dict
        request_to_store = {
            'host': request.get_host(),
            'path': request.path,
            'method': request.method,
            'uri': request.build_absolute_uri(),
            'user_agent': request.META.get('HTTP_USER_AGENT', None),
            'remote_addr': request.META.get('REMOTE_ADDR', None),
            'cookies': request.COOKIES,
            'get': request.GET,
            'post': request.POST,
            'raw_post': request.body,
        }
        SipmleRequest.objects.create(
            data=json.dumps(request_to_store)
        )
        return response
