from django import forms
from django.forms import fields

from core.models import Profile


class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    age = forms.IntegerField(min_value=4)
    gender = forms.CharField()
    city = forms.CharField()
    country = forms.CharField()



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    
