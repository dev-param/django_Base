from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from userapi.auth import verifier





UserModel = get_user_model()


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """    
        # Write Your Own Function Or just Use default
        `
            super().authenticate(request, username=username, password=password, kwargs=kwargs)
        ` 
         
        """

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
            verifier.checkIfAllowed(user)
        except UserModel.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
            
        verifier.LoginLog(user)





        
 