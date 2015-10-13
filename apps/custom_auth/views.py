from django.shortcuts import render

from custom_auth.models import User, SipmleRequest
from pprint import pprint

# Create your views here.
def index(request):
    user = User.objects.get(pk=1)

    return render(request, 'custom_auth/index.html', {'user': user})


def requests(request):
    last_requests = SipmleRequest.objects.all().order_by('-timestamp')[:10]
    # Mark as views
    SipmleRequest.objects.filter(pk__in=last_requests).update(viewed=True)
    return render(
        request,
        'custom_auth/requests.html',
        {'last_requests': last_requests}
    )