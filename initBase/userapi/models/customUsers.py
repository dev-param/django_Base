from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .jwt import JWT
from .tokenModels import AuthTokenModel

class CustomUsers(AbstractUser, PermissionsMixin):
    mobile_number = models.CharField(max_length=12)
    _active = models.JSONField(default=dict(status= True, detail= "Unknown Reason"))

    # for login with number or email
    # USERNAME_FIELD="email"    
    # extra_auth = models.ManyToManyField(ExtraAuthModel)

    # pending_task = models.ManyToManyField(PendingTaskModel)
    jwtSessions = models.ManyToManyField(AuthTokenModel)
    
    @property
    def is_active(self):
        return True
        # return self._active.get("status", False)
    
    def CreateToken(self):
        from .xAuth import XAuth
        xauth = XAuth.active.through.objects.filter(user__id=self.id)
        
        
        jwt_model = JWT(self.username)
        if xauth.exists():
    
            jwt_model.BasicVerificationToken(self, xauth)
            
     
        else:
            tokens = jwt_model.BasicAuthTokens()
            self.jwtSessions.add(tokens['authModel'])
            return {
                "access": tokens["access"].token,
                "refresh": tokens["refresh"].token
            }
    @classmethod
    def userByJwt(cls, token:str):
        return cls.objects.filter(jwtSessions__id= AuthTokenModel.objects.filter(tokenFiled__token=token).first().id)
