import requests
from userManagement.models import otpVerificationModel, MyUser
import random
from rest_framework.exceptions import NotAcceptable, PermissionDenied
from django.utils import timezone
from datetime import timedelta


def sendOtpWrapper(userModel, reasonId):



    
    userOtp = userModel.OtpField.filter(_at__date=timezone.now().date(), reason=reasonId)
    if not userOtp.exists():
        
        return sendSms(userModel, reasonId)

    
    if len(userOtp) > 50:
        raise NotAcceptable( {"status": "error", 'error': "User Blocked for 24 Hours"})
        
    last15min = userOtp.filter(_at__gt=timezone.now() - timedelta(minutes=15))

    if not last15min.exists():
        
        return sendSms(userModel, reasonId)


    if len(last15min) > 3:
        raise NotAcceptable(  {"status": "error", 'error': "User Blocked for 15 minute"})

    

    last2min = userOtp.filter(_at__gt=timezone.now() - timedelta(minutes=2))

    if  last2min.exists():
        raise NotAcceptable(  {"status": "error", 'error': "User Blocked for 2 minute"})
        
    else:
        
        return sendSms(userModel, reasonId)




def sendSms(userModel, reasonId):

    
    otpCode = str(random.randint(1111,9999))

    
    otpModel =   otpVerificationModel(
        otp=otpCode,
        reason=reasonId
        )
    otpModel.save()
    userModel.OtpField.add(otpModel)
    
    s = Fast2Sms(otpCode,userModel.mobile_number)
    if s.get("status", "error") == "success":
        otpModel.sendingStatus = True
        otpModel.info = {"status": "success", "data": s.get("data", "Info Not Available")}
        otpModel.save()
        return {"status": "success", "userResponse": "massage Sent Successfully" }
    else:
        otpModel.info = {"status": "error", "data": s.get("data", "Info Not Available")}
        otpModel.save()
        raise PermissionDenied(  {"status": "error", "userResponse": "massage not Sent Please Check Your number" })


        




    
    

def Fast2Sms(otpCode, number):
    
    payload = f"variables_values={otpCode}&route=otp&numbers={number}"
    headers = {
        'authorization': "ADD YOUR API HERE",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }
    try:
        response = requests.request(
                        "POST",
                        "https://www.fast2sms.com/dev/bulkV2",
                        data=payload,
                        headers=headers
                    )
        
        # print(response.text)
        if response.status_code == 200:
            return {"status": "success", "data": response.text}
        
        else:
            return {"status": "error", "data": response.text}
    except:
        print("add here support for admin reports")
        return {"status": "error", "data": "Server Error"}
        

