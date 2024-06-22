from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import RegexValidator
from django import forms

from .models import MyUser


class CustomUserCreationForm(UserCreationForm):
    
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = MyUser
        fields = ("mobile_number", "mobile_country_code",  "pin")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
  


class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = MyUser
        fields = ("mobile_number", "mobile_country_code", "pin", "_staff", "_active",  "password")





class CreateUserForm(forms.Form):

    username = forms.CharField(min_length=6, max_length=12, required=True)

    ph       = forms.CharField(
                    required=True,
                    label="Mobile Number", 
                    min_length=6,
                    max_length=10,
                    validators=[RegexValidator(
                        regex=r'^[0-9]+$',
                        message='Only digit characters are allowed.',
                    )]
                )
    pin = forms.CharField(min_length=4,
                    max_length=4,
                    validators=[RegexValidator(
                        regex=r'^[0-9]+$',
                        message='Only digit characters are allowed.',
                    )])
    dial_code = forms.CharField(
                    min_length=2,
                    max_length=5,
                    validators=[RegexValidator(
                        regex=r'^\+[0-9]+$',
                        message='Only [+1, +91, ...] characters are allowed.',
                    )])

    password = forms.CharField(
        label="Password", widget=forms.PasswordInput
    )


    

class LoginApiForm(forms.Form):
    ph  = forms.CharField(
                    required=True,
                    label="Mobile Number", 
                    min_length=6,
                    max_length=10,
                    validators=[RegexValidator(
                        regex=r'^[0-9]+$',
                        message='Only digit characters are allowed.',
                    )]
                )

    pin = forms.CharField(min_length=4,
                    max_length=4,
                    required=True,
                    validators=[RegexValidator(
                        regex=r'^[0-9]+$',
                        message='Only digit characters are allowed.',
                    )])
    
    otp = forms.CharField(min_length=4,
                    max_length=4,
                    required=False,
                    validators=[RegexValidator(
                        regex=r'^[0-9]+$',
                        message='Only digit characters are allowed.',
                    )])
    




class AuthTokenForm(forms.Form):
    token = forms.RegexField(r"^((?:\.?(?:[A-Za-z0-9-_]+)){3})$",required=True,max_length=999, min_length=200 )

