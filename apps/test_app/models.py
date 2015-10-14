from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    birthday = models.DateField(u'Birthday', blank=True, null=True)
    jubber_id = models.CharField(
        u'Jubber id',
        max_length=256,
        blank=True,
        null=True)
    skype_id = models.CharField(
        u'Skype id',
        max_length=256,
        blank=True,
        null=True)
    biography = models.TextField(u'Biography', blank=True, null=True)
    other_contacts = models.TextField(u'Other contacts', blank=True, null=True)

    class Meta:
        app_label = 'test_app'
