from django.shortcuts import render
from django.contrib.auth import get_user_model,authenticate, login
# from django.core.exceptions import BadRequest


from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework import status
# from rest_framework import exceptions
from .models import MyUser, otpVerificationModel
# from .userManagers import userManagers
# forms
from .forms import CreateUserForm, LoginApiForm


# date 
from django.utils import timezone
from datetime import timedelta

# pyjwt
import jwt


# basic local
from .basicLocal.sendOtp import sendOtpWrapper
from initBase.settings import SECRET_KEY
# Create your views here.
class BaseUserManagementApiView(APIView):

    pass


class UserManagementApiView(BaseUserManagementApiView):
    
    def responseRequest(self, data, statusCode=status.HTTP_200_OK):
        return Response(data=data, status=statusCode)

    def responseBadRequest(self, data, statusCode=status.HTTP_400_BAD_REQUEST):
        return Response(data=data, status=statusCode )    

class AuthUserManagementApiView(BaseUserManagementApiView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]







class CreateUserApiView(UserManagementApiView):

    def post(self, request, format=None):
        f = CreateUserForm(request.data)
        if f.is_valid():
            try:

                user = get_user_model().objects.get(mobile_number=f.cleaned_data['ph'])
                return self.responseRequest({"user": user.mobile_number})
            except get_user_model().DoesNotExist:
                
                user = get_user_model().objects.create_user(
                    mobile_number=f.cleaned_data['ph'],
                    pin=f.cleaned_data['pin'],
                    mobile_country_code=f.cleaned_data['dial_code'],
                    password=f.cleaned_data['password']
                )
                sendOtpWrapper(user)
                return self.responseRequest({"user": user.mobile_number})
            
                

            # Fast2Sms("45464", f.cleaned_data['ph'])
            # print(MyUser.objects.get(mobile_number=f.cleaned_data['ph']).is_staff)
         
            # print((f.cleaned_data['ph']))

            # sendOtpWrapper
            # newUser = MyUser.objects.create_user(
            #     mobile_number=f.cleaned_data['ph'],
            #     pin=f.cleaned_data['pin'],
            #     mobile_country_code=f.cleaned_data['dial_code'],
            #     password=f.cleaned_data['password']

            #     )
            # print(newUser.mobile_number)
            # newUser.save()
            
            
            
            
        return Response(f.errors.as_data())
    


# class CreateUserApiView(UserManagementApiView):

#     def post(self, request, format=None):
        


class LoginUserApiView(UserManagementApiView):
    def post(self, request, format=None):
        

        print(jwt.encode(
            payload={"kjh": "j"},
            key=jwt.base
        ))
        return Response()
        loginFormData = LoginApiForm(request.data)
        if not loginFormData.is_valid():
            
            return self.responseBadRequest({"error": loginFormData.errors.as_data()})
        
        
        user = authenticate(
            request=request, 
            mobile_number=loginFormData.cleaned_data.get("ph"), 
            pin=loginFormData.cleaned_data.get("pin"))
        if not user:
            return self.responseBadRequest({"error": "Username or Password not Valid"})

        if loginFormData.cleaned_data.get("otp") == "":
            s = sendOtpWrapper(user, reasonId="login")
            if s.get("status") == "error":
                return self.responseRequest({"success": s.get("error")})
            return self.responseRequest({"success": "otp generated successfully"})
            


        otpModel = user.OtpField.filter(_at__gt=timezone.now() - timedelta(minutes=15))
        if not otpModel.exists():
            return self.responseBadRequest({"error": "Wrong otp"})
 
        otpFV = otpModel.last()
        if loginFormData.cleaned_data.get("otp") == otpFV.otp:
            if  otpFV._Success:
                return self.responseBadRequest({"error": "otp already used"})
            otpFV._Success=True
            otpFV.save()

        
        # MyUser.objects.filter().last()
        
        
        # sendOtpWrapper(user, reasonId="login")
        
            
            
        return Response({})
