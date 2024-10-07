from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin



class CustomUsers(AbstractUser, PermissionsMixin):
    mobile_number = models.CharField(max_length=12)
    _active = models.JSONField(default=dict({"status": True, "detail": "Unknown Reason"}))

    # for login with number or email
    # USERNAME_FIELD="email"    
    # extra_auth = models.ManyToManyField(ExtraAuthModel)

    # pending_task = models.ManyToManyField(PendingTaskModel)
    
    @property
    def is_active(self):
        return self._active.get("status", False)
    
    def CreateToken(self):
        # self.pending_task.add()
        pass