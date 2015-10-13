from django.shortcuts import render

from custom_auth.models import User


# Create your views here.
def index(request):
    user = User.objects.get(pk=1)

    return render(request, 'custom_auth/index.html', {'user': user})


def requests(request):
    return render(request, 'custom_auth/requests.html')