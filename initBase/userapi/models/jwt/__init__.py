from typing import TypedDict
import uuid
import jwt

# date 
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from datetime import timedelta

from initBase.settings import SECRET_KEY
from ..tokenModels import AuthTokenModel, TokenModel
from userapi.exception import CustomAPIX, status
from userapi.auth.config import Config

class BATReturn(TypedDict):
    access: TokenModel
    refresh: TokenModel
    authModel: AuthTokenModel

class BVTReturn(TypedDict):
    pass

class JWT:

    def __init__(self, user_field):
        self.user_field = user_field
    def BasicVerificationToken(self,user, xauthList, authTokenModel=None )->BVTReturn:
        if authTokenModel is None:
            authTokenModel =  AuthTokenModel.objects.create()

        verification = self.create(
            "mfa",

        ) 
        authTokenModel.tokenFiled.add(
            verification
        )
        requireAuth = self.xauthFilter(xauthList, xauth__required=True)
        if requireAuth is not None:
            raise NotImplementedError("NOt set Here yet")
            # raise CustomAPIX({"mfaToken": verification.token, "code": requireAuth.xauth.name}, statusCode=status.HTTP_202_ACCEPTED)
        requireAuth = self.xauthFilter(xauthList, raiseError="Check Default_mfa in Config List" , xauth__name=Config.Default_mfa)
      

        Config().getPTEngine(requireAuth.xauth.name, raise_exception=True)(user).onTokenCreation(token=verification.token)

        raise CustomAPIX({"mfaToken": verification.token,  "code": requireAuth.xauth.name}, statusCode=status.HTTP_202_ACCEPTED)



        
        
        
    def xauthFilter(self, xauthList, raiseError=None, **kwargs):
        a = xauthList.filter(**kwargs)
        if not a.exists():
            if raiseError is not None:
                if isinstance(raiseError, str):
                    raise KeyError(raiseError)
                raise raiseError
            return None
        
        return a[0]


    def BasicAuthTokens(self, authTokenModel=None, remember_me=False)->BATReturn:
       
        if authTokenModel is None:
            authTokenModel =  AuthTokenModel.objects.create()
        
        

        access = self.create(
            "access",
            
        ) 
        refresh = self.create(
            "refresh",
            timedelta(days=7) if remember_me else timedelta(days=1)
            
        ) 
        
        authTokenModel.tokenFiled.add(
            access,
            refresh
        )
        return {
            "access": access,
            "refresh": refresh,
            "authModel": authTokenModel
        }


    def create(self, token_type = "verify", exp_at = timedelta(minutes=15)):
        _token_data = {
            "jti": str(uuid.uuid4()), 
            "iat":timezone.now(),
            "exp":timezone.now() + exp_at,

        }


        token = self.JwtEncode({   
                        "token_type": token_type,
                        "exp": _token_data['exp'],
                        "iat": _token_data['iat'],
                        "jti": _token_data['jti'],
                        "user": self.user_field
                    })
        
        return TokenModel.objects.create(
            token=token,
            token_type=token_type,
            jti=_token_data['jti'],
            expire_at= _token_data['exp'],
            iat=_token_data['iat']
            
        )

         
        




    def JwtEncode(self, data):

        return jwt.encode(data,SECRET_KEY, algorithm="HS256")


            
    

