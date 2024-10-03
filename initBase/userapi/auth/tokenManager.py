
from django.contrib.auth import get_user_model


UserModel = get_user_model()




class TokenManager:
    def __init__(self, user):
        self.user = user

    def createToken(self):
        pass
        