from django.shortcuts import render
from django.http import HttpResponse

from test_app.models import CustomUser, SipmleRequest
from dateutil import parser as date_parser

import json


def index(request):
    user = CustomUser.objects.first()

    return render(request, 'test_app/index.html', {'custom_user': user})


def requests(request):
    """
        Initial requests page
    """
    return render(
        request,
        'test_app/requests.html'
    )


def last_requests(request):
    """
        Api requests handler
        GET - returns or last 10 new request or
            new requests with timestamp more than in GET request parameter
        POST - Marks requests as viewed depanding on viewed_ids
    """
    if request.method == 'GET':
        last_requests = SipmleRequest.\
            objects.filter(viewed=False).\
            order_by('-timestamp')
        if request.GET.get('timestamp'):
            last_requests = last_requests.filter(
                timestamp__gte=date_parser.parse(request.GET.get('timestamp'))
            )
        else:
            last_requests = last_requests[:10]
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


def edit_user(request):
    return render(request, 'test_app/edit_user.html')


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
        request['id'] = item.pk
        serialized.append(request)
    return json.dumps(serialized)
