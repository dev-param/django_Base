from django.db import models


class TokenModel(models.Model):
    token_type = models.TextChoices("token_type", "ACCESS REFRESH TEMP")

    token = models.SlugField(max_length=1000)
    token_type = models.CharField(choices=token_type.choices)
    jti = models.CharField(max_length=200)
    expire_at = models.DateTimeField()
    iat = models.DateTimeField()



class AuthTokenModel(models.Model):
    tokenFiled = models.ManyToManyField(TokenModel)
    


    