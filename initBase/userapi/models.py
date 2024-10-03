from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

# Create your models here.

class CustomUsers(AbstractUser, PermissionsMixin):
    mobile_number = models.CharField(max_length=12)

    # for login with number or email
    # USERNAME_FIELD="email"    
    # extra_auth = models.ManyToManyField()

class ExtraAuthModel(models.Model):
    name = models.CharField(max_length=255)
    
class LogsModel(models.Model):
    _type_logs = models.TextChoices('_type_logs', 'DEBUG INFO AUTH')
    _type = models.CharField(choices=_type_logs.choices)
    _tag = models.CharField(default="system")
    _info = models.JSONField(default=dict)
    _at = models.DateTimeField(auto_now_add=True)
    _user = models.ForeignKey(CustomUsers, on_delete=models.CASCADE, null=True)
    @classmethod
    def loginFailedLog(cls,user,create:bool=False, _info:dict={}):
        if create:
            return cls.objects.create(
                _type = LogsModel._type_logs.AUTH,
                _tag = "loginFail",
                _info = _info,
                _user=user
            )
            
        return cls.objects.filter(_tag="loginFail", _user=user)