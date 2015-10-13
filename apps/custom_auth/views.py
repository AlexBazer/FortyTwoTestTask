from django.shortcuts import render
from django.http import HttpResponse
from custom_auth.models import User, SipmleRequest

import json

# Create your views here.
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