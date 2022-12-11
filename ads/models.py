from __future__ import unicode_literals
from django.db import models
import uuid
from django.utils.translation import ugettext_lazy as _
from cities_light.models import Country
from users.models import RegionName,CityName


class Category(models.Model):
    name = models.CharField(max_length=128,unique=True)
    image = models.ImageField()

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name


class Property(models.Model):
    property_name = models.CharField(max_length=128,unique=True)
    property_symbol = models.CharField(max_length=128)

    class Meta:
        ordering = ['property_name']
        verbose_name_plural = 'Properties'

    def __unicode__(self):
        return self.property_name



class PropertyValue(models.Model):
    property_ptr = models.ForeignKey(Property)
    property_value = models.DecimalField(default=0.0,decimal_places=2, max_digits=15)

    class Meta:
        ordering = ['property_value']

    def get_pk(self):
        return str(self.pk)
        
    def __unicode__(self):
        return str(self.property_value)


class Label(models.Model):
    label_name = models.CharField(max_length=128,unique=True)

    def __unicode__(self):
        return self.label_name


class LabelValue(models.Model):
    label = models.ForeignKey(Label) 
    label_value = models.CharField(max_length=128)

    def __unicode__(self):
        return self.label_value


class Price(models.Model):
    price = models.DecimalField(default=0.0,decimal_places=2, max_digits=15,unique=True)

    class Meta:
        ordering = ['price']

    def __unicode__(self):
        return str(self.price)

   
class SubCategory(models.Model):
    category = models.ForeignKey(Category)
    subcategory_name = models.CharField(max_length=128)
    image = models.ImageField()
    property_ptr = models.ManyToManyField(Property,blank=True)
    label = models.ManyToManyField(Label,blank=True)
    has_price = models.BooleanField(default=False)
    is_job = models.BooleanField(default=False)

    class Meta:
        ordering = ['subcategory_name']
        verbose_name_plural = 'SubCategories'

    def __unicode__(self):
        return self.subcategory_name


class Currency(models.Model):
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=128)
    ISO_Code = models.CharField(max_length=128,blank=True,null=True)

    def __unicode__(self):
        if self.ISO_Code == None:
            return "USD"
        else:
            return self.ISO_Code


class Advertisement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    date_added = models.DateTimeField(auto_now_add=True)    
    date_updated = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users.MyUser',null=True,blank=True)
    title = models.CharField(max_length=128)
    description = models.TextField(null=True,blank=True)
    country = models.ForeignKey(Country)
    region = models.ForeignKey(RegionName)
    city = models.ForeignKey(CityName,null=True,blank=True)
    image1 = models.ImageField()
    image2 = models.ImageField(null=True,blank=True)
    image3 = models.ImageField(null=True,blank=True)
    image4 = models.ImageField(null=True,blank=True)
    category = models.ForeignKey(Category,null=True)
    subcategory = models.ForeignKey(SubCategory,null=True)
    label_value = models.ManyToManyField(LabelValue)
    property_value = models.ManyToManyField(PropertyValue)
    currency = models.ForeignKey(Currency,blank=True)
    price = models.DecimalField(default=0.0,decimal_places=2, max_digits=15,blank=True)
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    active = models.BooleanField(default=True)
    premium = models.BooleanField(default=False)

    class Meta:
        ordering = ['-premium','date_updated']







