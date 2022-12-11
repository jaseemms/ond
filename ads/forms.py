from django import forms
from django.forms.widgets import TextInput, Select, Textarea, FileInput
from django.utils.translation import ugettext_lazy as _
from ads.models import Advertisement,LabelValue, PropertyValue


class AdvertisementForm(forms.ModelForm):
    
    class Meta:
        model = Advertisement
        exclude = ['user','active','premium','date_added','date_updated','label_value','property_value']
        widgets = {
            'title': TextInput(attrs={'placeholder' : 'Title'}),
            'description': Textarea(attrs={'placeholder' : 'Description'}),
            'country': Select(attrs={'placeholder' : 'Country'}),
            'region': Select(attrs={'placeholder' : 'Region'}),
            'city': Select(attrs={'placeholder' : 'City'}),
            'category': Select(attrs={'placeholder' : 'Category'}),
            'subcategory': Select(attrs={'placeholder' : 'Subcategory'}),
            'currency': Select(attrs={'placeholder' : 'Currency'}),
            'price': TextInput(attrs={'placeholder' : 'Price'}),
            'image1': FileInput(),
            'image2': FileInput(),
            'image3': FileInput(),
            'image4': FileInput(),
            'name': TextInput(attrs={'placeholder' : 'Name'}),
            'phone': TextInput(attrs={'placeholder' : 'Phone'}),
        }
        error_messages = {
            'title' : {
                'required' : _("Title field is required.")
            },
            'description' : {
                'required' : _("Description field is required.")
            },
            'country' : {
                'required' : _("Country field is required")
            },
            'region' : {
                'required' : _("Region field is required")
            },
            'city' : {
                'required' : _("City field is required")
            },
            'image1' : {
                'required' : _("Image1 field is required.")
            },
            'name' : {
                'required' : _("Name field is required.")
            },
            'phone' : {
                'required' : _("Phone field is required")
            }
        }

    def __init__(self, *args, **kwargs):
        super(AdvertisementForm, self).__init__(*args, **kwargs)
        self.fields['country'].empty_label = 'Select Country'
        self.fields['region'].empty_label = 'Select Region'
        self.fields['city'].empty_label = 'Select City'
        self.fields['category'].empty_label = 'Select Category'
        self.fields['subcategory'].empty_label = 'Select Subcategory'
        self.fields['currency'].empty_label = 'Select Currency'


class FilterAdvertisementForm(forms.ModelForm):
    
    class Meta:
        model = Advertisement
        exclude = ['user','active','premium','date_added','date_updated','label_value',
        'property_value','title','description','price','currency','image1','image2','image13','image4',
        'name','phone']

        widgets = {
            'country': Select(attrs={'placeholder' : 'Country'}),
            'region': Select(attrs={'placeholder' : 'Region'}),
            'city': Select(attrs={'placeholder' : 'City'}),
            'category': Select(attrs={'placeholder' : 'Category'}),
            'subcategory': Select(attrs={'placeholder' : 'Subcategory'})
        }
        
    def __init__(self, *args, **kwargs):
        super(FilterAdvertisementForm, self).__init__(*args, **kwargs)
        self.fields['country'].empty_label = 'All Countries'
        self.fields['region'].empty_label = 'All Regions'
        self.fields['city'].empty_label = 'All Cities'
        self.fields['category'].empty_label = 'All Categories'
        self.fields['subcategory'].empty_label = 'All Subcategories'
        self.fields['country'].required = False
        self.fields['region'].required = False
        self.fields['city'].required = False
        self.fields['category'].required = False
        self.fields['subcategory'].required = False