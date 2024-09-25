from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

# Create your models here.

class CustomUsers(AbstractUser, PermissionsMixin):
    mobile_number = models.CharField(max_length=12)
    
