from django.db import models 
from django.contrib.auth import get_user_model
USER_MODEL = get_user_model()
class XAuth(models.Model):
    name = models.CharField(max_length=255)
    config = models.JSONField(default=dict, blank=True)
    required = models.BooleanField(default=False)
    
    active = models.ManyToManyField(
        USER_MODEL,
        through="XAuthSetup",
        through_fields=("xauth", "user"),
    )
    def __str__(self) -> str:
        return self.name



class XAuthSetup(models.Model):
    xauth = models.ForeignKey(XAuth, on_delete=models.CASCADE)
    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)

    # required = models.BooleanField(default=False)


