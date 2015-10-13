from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User)
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


class SipmleRequest(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.TextField('Required request data in json format')
    viewed = models.BooleanField('Data is viewed', default=False)

    def __unicode__(self):
        return self.timestamp.isoformat()
