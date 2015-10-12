import json


class SaveRequestMiddleware(object):
    def process_response(self, request, response):
        return response        
        # request_to_store = {
        #     'host': request.get_host(),
        #     'path': request.path,
        #     'method': request.method,
        #     'uri': request.build_absolute_uri(),
        #     'user_agent': request.META.get('HTTP_USER_AGENT', None),
        #     'remote_addr': request.META.get('REMOTE_ADDR', None),
        #     'cookies': request.COOKIES,
        #     'get': request.GET,
        #     'post': request.POST,
        #     'raw_post': request.body,
        #     'is_secure': request.is_secure(),
        #     'is_ajax': request.is_ajax(),
        # }
        # print json.dumps(request_to_store)