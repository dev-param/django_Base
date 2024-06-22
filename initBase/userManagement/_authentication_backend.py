from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied
import jwt
from initBase.settings import SECRET_KEY

from icecream import ic
from .models import JwtAuthToken
from .jwt_auth import GetUserWithJwtAccess

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, mobile_number=None, pin=None, **k):
        user = self.getUserWithPIN(mobile_number=mobile_number, pin=pin)
        
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
            raise NotAuthenticated

        
        token = authorization_header.split(' ')[1]
        
        JwtAuthTokenModel= GetUserWithJwtAccess(token=token)

        user = JwtAuthTokenModel.for_user
        if  not user.is_active:
            

            raise PermissionDenied({"code": "User Inactive", "detail": user._active.get('detail', "Contact Us for More Information")})
        
        if  JwtAuthTokenModel.is_destroyed:
            raise AuthenticationFailed
        if  JwtAuthTokenModel.is_banned:
            raise PermissionDenied({"code": "Suspicious Activity Detected", "detail": JwtAuthTokenModel._banned.get('detail', "Contact Us for More Information")})
        
        return (user, token)
    




