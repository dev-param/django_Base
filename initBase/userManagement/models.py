from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .userManagers import userManagers
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.


numeric_validator = RegexValidator(
    regex=r'^[0-9]+$',
    message='Only digit characters are allowed.',
)





class walletModel(models.Model):
    transition_id = models.CharField(unique=True)


class otpVerificationModel(models.Model):
    otp = models.CharField(max_length=4)
    reason = models.CharField(max_length=50)
    sendingStatus = models.BooleanField(default=False)
    _Success = models.BooleanField(default=False)
    info = models.JSONField(default=dict)
    _at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.otp} {self.reason}"


class MyUser(AbstractBaseUser, PermissionsMixin):
    first_name = None
    last_name = None
    is_superuser = models.BooleanField(default=False)
    _staff = models.JSONField(default=dict({"status": False}))
    _active = models.JSONField(default=dict({"status": False}))
    date_joined = models.DateTimeField(default=timezone.now)


    pin = models.CharField(default=0000, validators=[
            MinLengthValidator(4, "4 Numbers PIN Allowed"),
            
        ], max_length=4)
    Wallet = models.ManyToManyField(walletModel, editable=False)

    # mobile number
    mobile_number = models.CharField(unique=True, max_length=12, validators=[MinLengthValidator(6, "Required six numbers")])
    mobile_country_code = models.CharField(default="+91", max_length=5, validators=[MinLengthValidator(2, "Required Two numbers")])
    
    OtpField = models.ManyToManyField(otpVerificationModel)

   


    objects = userManagers()
    USERNAME_FIELD = "mobile_number"
    REQUIRED_FIELDS = ["pin"]

    def __str__(self):
        return self.mobile_number
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self._staff.get("status")
    
    @property
    def is_active(self):
        return self._active.get("status")
    



class AccessTokenModel(models.Model):
    token = models.SlugField(max_length=1000)
    jti = models.CharField(max_length=200)
    expire_at = models.DateTimeField()
    _at = models.DateTimeField(auto_now_add=True)

class RefreshTokenModel(models.Model):
    token = models.SlugField(max_length=1000)
    jti = models.CharField(max_length=200)
    expire_at = models.DateTimeField()
    _at = models.DateTimeField(auto_now_add=True)

class userAuthToken(models.Model):

    access_token = models.ForeignKey(AccessTokenModel, on_delete=models.CASCADE)
    refresh_token = models.ForeignKey(RefreshTokenModel, on_delete=models.CASCADE)
    _banned = models.JSONField(default=dict)
    for_user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    @property
    def is_banned(self):
        return self._banned.get("status")