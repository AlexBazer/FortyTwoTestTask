from django.contrib import admin
from apps.test_app.models import CustomUser


admin.site.register(CustomUser)
