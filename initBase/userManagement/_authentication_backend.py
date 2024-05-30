from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest



class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, mobile_number=None, pin=None):
        user = self.getUserWithPIN(mobile_number=mobile_number, pin=pin)
        # print(getattr(user, "is_active"))
        if user:
            return user
        return None

    def getUserWithPIN(self, mobile_number, pin):
        try:
            return get_user_model().objects.get(mobile_number=mobile_number, pin=pin)
        except get_user_model().DoesNotExist:
            return None
