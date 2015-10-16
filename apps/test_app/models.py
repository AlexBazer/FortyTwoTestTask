from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    birthday = models.DateField(u'Birthday', blank=True, null=True)
    jabber_id = models.CharField(
        u'jabber id',
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
    photo = models.ImageField(u'User Proto', upload_to='photos')

    class Meta:
        app_label = 'test_app'


class SipmleRequest(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.TextField('Required request data in json format')
    viewed = models.BooleanField('Data is viewed', default=False)

    class Meta:
        app_label = 'test_app'
