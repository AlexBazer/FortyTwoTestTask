import json

from custom_auth.models import SipmleRequest


class SaveRequestMiddleware(object):
    def process_response(self, request, response):
        # Collect all meta except wsgi objects
        meta = {}
        for key in request.META:
            if not key.startswith('wsgi'):
                meta[key] = request.META[key]

        # Collect request data to the dict
        request_to_store = {
            'host': request.get_host(),
            'path': request.path,
            'method': request.method,
            'uri': request.build_absolute_uri(),
            'user_agent': meta.pop('HTTP_USER_AGENT', None),
            'remote_addr': meta.pop('REMOTE_ADDR', None),
            'cookies': request.COOKIES,
            'get': request.GET,
            'post': request.POST,
            'raw_post': request.body,
        }
        SipmleRequest.objects.create(
            data=json.dumps(request_to_store)
        )
        return response
