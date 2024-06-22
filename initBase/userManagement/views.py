# python
import uuid

from django.shortcuts import render, HttpResponse
from django.contrib.auth import get_user_model,authenticate, login
# from django.core.exceptions import BadRequest


from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotAcceptable,ValidationError 
from .models import JwtAuthToken
# from .userManagers import userManagers
# forms
from .forms import CreateUserForm, LoginApiForm, AuthTokenForm


# date 
from django.utils import timezone
from datetime import timedelta

# pyjwt
import jwt


# basic local
from .basicLocal.sendOtp import sendOtpWrapper
from initBase.settings import SECRET_KEY
from ._authentication_backend import CustomTokenAuth
from .jwt_auth import CreateJwtToken, UpdateRefreshToken
from icecream import ic
# Create your views here.





class BaseUserManagementApiView(APIView):

    pass


class UserManagementApiView(BaseUserManagementApiView):
    
    def responseRequest(self, data, statusCode=status.HTTP_200_OK):
        return Response(data=data, status=statusCode)

    def responseBadRequest(self, data, statusCode=status.HTTP_400_BAD_REQUEST):
        return Response(data=data, status=statusCode )    

class AuthUserManagementApiView(BaseUserManagementApiView):
    authentication_classes = [CustomTokenAuth]
    # permission_classes = [permissions.IsAdminUser]


    pass




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
    





class RefreshTokenApiView(UserManagementApiView):

    def post(self, request, format=None):
        
        requestData = AuthTokenForm(request.data)
        
        if not requestData.is_valid():
            raise ValidationError({"detail": requestData.errors.as_data()})
        
        
        return Response(UpdateRefreshToken(requestData.cleaned_data.get("token")))
        


class LoginUserApiView(UserManagementApiView):
    def post(self, request, format=None):
        
        
        

        
        loginFormData = LoginApiForm(request.data)
        if not loginFormData.is_valid():
            
            raise AuthenticationFailed({"detail": loginFormData.errors.as_data()})
        
        
        user = authenticate(
            request=request, 
            mobile_number=loginFormData.cleaned_data.get("ph"), 
            pin=loginFormData.cleaned_data.get("pin"))
        if not user:
            raise AuthenticationFailed({"detail": "Username or Password not Valid"})
        if not user.is_active:
            raise AuthenticationFailed({"detail": user._active.get("detail", "Contact Us for More Information")})
        
        
        if loginFormData.cleaned_data.get("otp") == "":
            s = sendOtpWrapper(user, reasonId="login")
            if s.get("status") == "error":
                return self.responseRequest({"success": s.get("detail")})
            return self.responseRequest({"success": "otp generated successfully"})
            


        otpModel = user.OtpField.filter(_at__gt=timezone.now() - timedelta(minutes=15))
        if not otpModel.exists():
            raise AuthenticationFailed({"detail": "Wrong otp"})
 
        otpFV = otpModel.last()
        if loginFormData.cleaned_data.get("otp") == otpFV.otp:
            if  otpFV._Success:
                raise AuthenticationFailed({"detail": "otp already used"})
            otpFV._Success=True
            otpFV.save()
            
            

        jwtTokenModel =  CreateJwtToken(user)
            
        return Response({
            "access":  jwtTokenModel.access_token.token,
            "refresh_token": jwtTokenModel.refresh_token.token
        })

     





class ProfileApi(AuthUserManagementApiView):
    def post(self, request, format=None):

        u = request.user
        return Response({
            "mobile number": u.mobile_number,
            "active sessions": JwtAuthToken.objects.filter(for_user_id=u.id).count()
        })


class UserLogout(AuthUserManagementApiView):
    def post(self, request, format=None):

        JwtAuthToken.objects.filter(access_token__token=request.auth).update(_banned={"status": True, "code": "self"})
        return Response({"detail": "Session Destroy successfully"})
    
