
from django.contrib.auth.forms import UsernameField
from django import forms
from .models import CustomUsers



class LoginForm(forms.Form):
    # username = forms.CharField( max_length=50, required=True)
    username = UsernameField()
    password = forms.CharField(max_length=99)




class XAuthForm(forms.Form):
    mfaToken = forms.RegexField(
        regex=r'^[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+$',
        error_messages={'detail': 'Invalid JWT token format'}
    )
    code = forms.SlugField()
