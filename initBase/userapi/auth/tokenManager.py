import uuid


from django.contrib.auth import get_user_model



import jwt


from initBase.settings import SECRET_KEY
from userapi.models import  AuthTokenModel

# date 
from django.utils import timezone
from datetime import timedelta

UserModel = get_user_model()




class TokenManager:
    def __init__(self, user):
        self.user = user


    




    def createToken(self, **kwargs):

        """
        **kwargs
            exp_at=1 #refresh token live
        """


        # AuthTokenModel.objects.create()

        # access_token = self.CreateJwtToken(
        #     "access",
        #     )




        # pt = PendingTaskManager(self.user).get_pending_task()
        # if pt:
        #     # ic(pt[0].task_name)
        #     engine = Config().getPTEngine(pt[0].task_name)
  
            
        #     XAuthHandlerBase(self.user, engine).sender()
            # raise CustomAPIX("Please Complete First Pending Task", statusCode=status.HTTP_202_ACCEPTED)

        # exp_at = kwargs.get("exp_at", 1)
        # if not isinstance(exp_at, int):
        #     raise ValueError("exp_at must be an integer")
    



    def CreateJwtToken(self, token_type, exp=timedelta(minutes=15), user="" ):
        return jwt.encode({
            "token_type": token_type,
            "exp": timezone.now() + exp,
            "iat": timezone.now(),
            "jti": str(uuid.uuid4()),
            "user": user, 
        },
        SECRET_KEY,
        algorithm="HS256"
        )

        # access_token = JwtEncode({   
                                    # "token_type": "access",
                                    # "exp": access_token_data['exp'],
                                    # "iat": access_token_data['iat'],
                                    # "jti": access_token_data['jti'],
                                    # "user": user.mobile_number
                                # })
        
        
                
        # refresh_token = JwtEncode({   
                                        # "token_type": "refresh",
                                        # "exp": refresh_token_data['exp'],
                                        # "iat": refresh_token_data['iat'],
                                        # "jti": refresh_token_data['jti'],
                                        # "user": user.mobile_number
                                    # })

        