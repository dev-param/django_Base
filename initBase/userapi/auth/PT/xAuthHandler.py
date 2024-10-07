from userapi.models import LogsModel
import random
from .pTEngines import PTEnginesBase
# from rest_framework.exceptions import 

class XAuthHandlerBase:

    def __init__(self, user, engine:PTEnginesBase):
        self.user = user
        self.engine = engine(user)

   
    def sender(self):
     
        otpCode = str(random.randint(1111,9999))
        LogsModel.xAuthModel(
            self.user,
            _info= {
                "otp": otpCode,
            }
        )
        self.engine.send(otpCode)





        # if self.SenderEngine is None:
        #     ic("Sender Engine not Setup")
        #     ic(f"for debugging code is: {otpCode}")
             
          

        
