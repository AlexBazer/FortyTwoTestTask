from django.shortcuts import render

from apps.test_app.models import CustomUser


# Create your views here.
def index(request):
    user = CustomUser.objects.first()

    return render(request, 'test_app/index.html', {'user': user})
