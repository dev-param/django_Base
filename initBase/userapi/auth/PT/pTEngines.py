import random
from django.utils import timezone
from datetime import timedelta
from userapi.task import sendMobileOtp
class PTEnginesBase:
    
    def __init__(self, user):
        self.user = user

    def onTokenCreation(self, **kwargs):
        self.send(**kwargs)


    def send(self, **kwargs):
        ic("This is just debug testing you Make Your Own class")
        ic(f"for debugging code is: {kwargs.data}")


class MobilePTEngine(PTEnginesBase):
    def send(self, token):
        from userapi.models import LogsModel
        from userapi.auth.verifier import isTimeBlocked


        
        otp = random.randint(1111, 9999)

        sendMobileOtp(otp, self.user.mobile_number)
        LogsModel.otpLog(
            token,
            otp,
            self.user,    
        )