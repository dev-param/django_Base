from django.db import models
from .customUsers import CustomUsers

# date 
from django.utils import timezone
from datetime import timedelta

class LogsModel(models.Model):
    _type_logs = models.TextChoices('_type_logs', 'INFO AUTH XAUTH')
    _type = models.CharField(choices=_type_logs.choices)
    _tag = models.CharField(default="system")
    _info = models.JSONField(default=dict)
    _at = models.DateTimeField(auto_now_add=True)
    _user = models.ForeignKey(CustomUsers, on_delete=models.CASCADE, null=True)
    @classmethod
    def loginFailedLog(cls,user,create:bool=False, _info={}):
        if create:
            return cls.objects.create(
                _type = LogsModel._type_logs.AUTH,
                _tag = "loginFail",
                _info = _info,
                _user=user
            )
            
        return cls.objects.filter(_tag="loginFail", _user=user)
    
    @classmethod
    def xAuthModel(cls, user, create:bool=False, _info=dict):
        _info.setdefault("exp_at", (timezone.now() - timedelta(minutes=15)))
        
        if create:
            pass
            # return cls.objects.create()
