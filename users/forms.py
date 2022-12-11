from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
from django.forms.widgets import TextInput, Select, Textarea
from django.utils.translation import ugettext_lazy as _
from users.models import MailBox,MyUser


class MailBoxForm(forms.ModelForm):

    class Meta:
        model = MailBox
        fields = ('message','phone')
        widgets = {
            'message': Textarea(attrs={'placeholder' : 'Message'}),
            'phone': TextInput(attrs={'placeholder' : 'Phone Number'}),
        }


class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = UserCreationForm.Meta.fields + ('name','phone','email','country','region','city')

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields.pop('password2')
        self.fields['country'].empty_label = 'Select Country'
        self.fields['region'].empty_label = 'Select Region'
        self.fields['city'].empty_label = 'Select City'
   
    def save(self,commit=True):
        return super(MyUserCreationForm, self).save()
        if commit:
            user.save()
        return user
  

class MyUserChangeForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ('username','name','phone','email','country','region','city')
    
    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['country'].empty_label = 'Select Country'
        self.fields['region'].empty_label = 'Select Region'
        self.fields['city'].empty_label = 'Select City'

