from django.shortcuts import render
from django.http import HttpResponse
from custom_auth.models import User, SipmleRequest

import json


def index(request):
    user = User.objects.get(pk=1)

    return render(request, 'custom_auth/index.html', {'user': user})


def requests(request):
    return render(
        request,
        'custom_auth/requests.html'
    )


def last_requests(request):

    return HttpResponse(
        json.dumps({'status': 'OK'}),
        content_type='application/json'
    )


def serialize_requests(requests):
    """
        Serialize requests
        :type QuestSet:requests 
    """
    serialized = []
    for item in requests:
        request = {}
        request['timestamp'] = item.timestamp.isoformat()
        request['data'] = item.data
        request['viewed'] = item.viewed
        serialized.append(request)
    return serialized