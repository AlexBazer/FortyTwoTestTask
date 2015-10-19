from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files import File

from PIL import Image
from StringIO import StringIO


class CustomUser(AbstractUser):
    RESIZE_WIDTH = 200,
    RESIZE_HEIGHT = 200

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
    photo = models.ImageField(
        u'User Proto',
        upload_to='photos',
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if self.photo:
            image = Image.open(StringIO(self.photo.read()))
            image.thumbnail(
                (self.RESIZE_WIDTH, self.RESIZE_HEIGHT),
                Image.ANTIALIAS
            )
            output = StringIO()
            image.save(
                output,
                format=image.format,
                quality=100,
                optimize=True,
                progressive=True
            )
            output.seek(0)
            self.photo = File(output, self.photo.name)
        super(CustomUser, self).save(*args, **kwargs)

    class Meta:
        app_label = 'test_app'


class SipmleRequest(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.TextField('Required request data in json format')
    viewed = models.BooleanField('Data is viewed', default=False)

    class Meta:
        app_label = 'test_app'
