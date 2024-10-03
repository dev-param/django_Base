
from django.contrib.auth.forms import UsernameField
from django import forms
from .models import CustomUsers



class LoginForm(forms.Form):
    # username = forms.CharField( max_length=50, required=True)
    username = UsernameField()
    password = forms.CharField(max_length=99)
