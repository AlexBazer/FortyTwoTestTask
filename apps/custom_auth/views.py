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
    if request.method == 'GET':
        last_requests = SipmleRequest.objects.filter(viewed=False).order_by('-timestamp')[:10]
        return HttpResponse(
            serialize_requests(last_requests),
            content_type='application/json'
        )
    elif request.method == 'POST' and request.is_ajax():
        viewed_requests = json.loads(request.body)
        viewed_reqeust_ids = []
        if viewed_requests:
            viewed_reqeust_ids = viewed_requests.get('viewed_ids', [])

        SipmleRequest.objects.filter(pk__in=viewed_reqeust_ids).\
            update(viewed=True)

        return HttpResponse(
            json.dumps({'status': 'ok'}),
            content_type='application/json'
        )

    return HttpResponse("Method not allowed", status=405)


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
    return json.dumps(serialized)