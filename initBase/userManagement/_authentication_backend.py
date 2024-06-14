from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from initBase.settings import SECRET_KEY


from .models import JwtAuthToken


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, mobile_number=None, pin=None, **k):
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



class CustomTokenAuth(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        if not authorization_header or not authorization_header.startswith('Bearer '):
            return None  

        print(authorization_header)
        token = authorization_header.split(' ')[1]
        try:

            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if decoded_token['token_type'] != "access":
                raise AuthenticationFailed('Token Type Invalid')

            return (JwtAuthToken.objects.get(access_token=token).for_user, token)
            
        except jwt.exceptions.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.DecodeError:
            raise AuthenticationFailed('Error decoding token')
        except JwtAuthToken.DoesNotExist:
            raise AuthenticationFailed('No such user')

        # return None
