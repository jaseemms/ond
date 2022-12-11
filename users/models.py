from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
import uuid
from cities_light.models import Country
from cities_light.models import City,Region


class RegionName(Region):
    class Meta:
        proxy = True

    def __unicode__(self):
        return self.name_ascii

class CityName(City):
    class Meta:
        proxy = True

    def __unicode__(self):
        return self.name_ascii


class MyUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    first_name = None
    last_name = None
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    email = models.EmailField(max_length=70,null=True,blank=True)
    country = models.ForeignKey(Country,null=True)
    region = models.ForeignKey(RegionName,null=True)
    city = models.ForeignKey(CityName,null=True,blank=True)

    class Meta:
        ordering = ['name']



class MailBox(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    to = models.ForeignKey(MyUser,related_name='to')
    ad = models.ForeignKey('ads.Advertisement')
    message = models.TextField()
    phone = models.CharField(max_length=128)
    is_read = models.BooleanField(default=False)
    creator = models.ForeignKey(MyUser,null=True,related_name='creator')
    date = models.DateTimeField(auto_now_add=True)
    inbox_deleted = models.BooleanField(default=False)
    sentitems_deleted = models.BooleanField(default=False)

    class Meta:
        ordering =['date']
	

