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
    expire_at = models.DateTimeField(null=True)
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
    def otpLog(cls, for_token, otp, user, expire_in=timedelta(minutes=15)):
        cls.objects.create(
                            _type = LogsModel._type_logs.XAUTH,
                            _tag = "otp",
                            _info = {
                                        "for_token": for_token,
                                        "otp": otp
                                    },
                            expire_at=timezone.now()+expire_in,
                            _user=user
        )
    @classmethod
    def filterOtpLog(cls, user):
        return cls.objects.filter(
                            _type = LogsModel._type_logs.XAUTH,
                            _tag = "otp",
                            _user=user
                            
        )
