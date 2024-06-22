# python
import uuid

from rest_framework.exceptions import AuthenticationFailed, PermissionDenied

import jwt
from django.utils import timezone
from datetime import timedelta

# local 
from initBase.settings import SECRET_KEY
from .models import JwtAuthToken, AccessTokenModel, RefreshTokenModel
from django.contrib.auth import get_user_model



from icecream import ic

def JwtEncode(data):

    return jwt.encode(data,SECRET_KEY, algorithm="HS256")

def CreateJwtToken(user, remember_me=True):
    
    exp_at = remember_me if 8 else 1

    
  
    try:

        access_token_data = {
            "jti": str(uuid.uuid4()), 
            "iat":timezone.now(),
            "exp":timezone.now() + timedelta(minutes=150),

        }
        refresh_token_data = {
            "jti": str(uuid.uuid4()), 
            "iat":timezone.now(),
            "exp":timezone.now() + timedelta(days=exp_at),

        }


    

        access_token = JwtEncode({   
                                    "token_type": "access",
                                    "exp": access_token_data['exp'],
                                    "iat": access_token_data['iat'],
                                    "jti": access_token_data['jti'],
                                    "user": user.mobile_number
                                })
        
        
                
        refresh_token = JwtEncode({   
                                        "token_type": "refresh",
                                        "exp": refresh_token_data['exp'],
                                        "iat": refresh_token_data['iat'],
                                        "jti": refresh_token_data['jti'],
                                        "user": user.mobile_number
                                    })
        

        ATModel =  AccessTokenModel.objects.create(
            token=access_token,
            jti=access_token_data['jti'],
            expire_at=access_token_data['exp'],
            iat= access_token_data['iat']

        )
        RTModel = RefreshTokenModel.objects.create(
            token=refresh_token,
            jti=refresh_token_data['jti'],
            expire_at=refresh_token_data['exp'],
            iat= refresh_token_data['iat']

        )
    
        return JwtAuthToken.objects.create(
            access_token=ATModel,
            refresh_token=RTModel,
            for_user=user,
            )

    except:
        raise AuthenticationFailed("unexpected error contact us")

        

def GetUserWithJwtAccess(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if decoded_token['token_type'] != "access":
            raise AuthenticationFailed('Token Type Invalid')
        return JwtAuthToken.objects.get(access_token__token=token)
       
    except jwt.exceptions.ExpiredSignatureError:
        raise AuthenticationFailed("Token has expired")
    except jwt.DecodeError:
        raise AuthenticationFailed('Error decoding token')
    except JwtAuthToken.DoesNotExist:
        raise AuthenticationFailed('No such user')

def GetUserWithJwtRefresh(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if decoded_token['token_type'] != "refresh":
            raise AuthenticationFailed('Token Type Invalid')
        return JwtAuthToken.objects.get(refresh_token__token=token)
       
    except jwt.exceptions.ExpiredSignatureError:
        raise AuthenticationFailed("Token has expired")
    except jwt.DecodeError:
        raise AuthenticationFailed('Error decoding token')
    except JwtAuthToken.DoesNotExist:
        raise AuthenticationFailed('No such user')

def UpdateRefreshToken(token):
    
    access_token_data = {
            "jti": str(uuid.uuid4()), 
            "iat":timezone.now(),
            "exp":timezone.now() + timedelta(minutes=150),

        }
    refresh_token_data = {
            "jti": str(uuid.uuid4()), 
        }
    jwtModel = GetUserWithJwtRefresh(token)
    user = jwtModel.for_user

    if  not user.is_active:
            
        raise PermissionDenied({"code": "User Inactive", "detail": user._active.get('detail', "Contact Us for More Information")})
        
    if  jwtModel.is_destroyed:
        raise AuthenticationFailed
    if  jwtModel.is_banned:
        raise PermissionDenied({"code": "Suspicious Activity Detected", "detail": jwtModel._banned.get('detail', "Contact Us for More Information")})
        

    access_token = JwtEncode({   
                                    "token_type": "access",
                                    "exp": access_token_data['exp'],
                                    "iat": access_token_data['iat'],
                                    "jti": access_token_data['jti'],
                                    "user": user.mobile_number
                                })
        
        
                
    refresh_token = JwtEncode({   
                                        "token_type": "refresh",
                                        "exp": jwtModel.refresh_token.expire_at,
                                        "iat": jwtModel.refresh_token.iat,
                                        "jti": refresh_token_data['jti'],
                                        "user": user.mobile_number
                                    })




    accessModel = AccessTokenModel.objects.filter(id=jwtModel.access_token.id)
    refreshModel = RefreshTokenModel.objects.filter(id=jwtModel.refresh_token.id)
    accessModel.update(
        token=access_token,
        jti=access_token_data['jti'],
        expire_at=access_token_data['exp'],
        iat= access_token_data['iat']
        )
    refreshModel.update(
        token=refresh_token,
        jti=refresh_token_data['jti'],

    )
    return {
        "access": accessModel[0].token,
        "refresh": refreshModel[0].token
    }
    




