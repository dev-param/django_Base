from django.contrib.auth import authenticate, get_user_model

# drf
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import exceptions

from .base import MainAPIView
# locals
from userapi.forms import LoginForm, XAuthForm

# Create your views here.

    


class LoginAPIView(MainAPIView):
    def post(self, request:Request):
       
        
        formData = LoginForm(request.data)
  
        if not formData.is_valid():
            raise self.parseError(exceptions.ValidationError, "Username Or Password Not Valid !", formData.errors.as_json(escape_html=True))
        

        user = authenticate(request, username=formData.cleaned_data['username'], password=formData.cleaned_data['password'])
        if user is None:
            raise self.parseError(exceptions.ValidationError, "Username Or Password Not Valid !")
 
        
        

        


        return Response(user.CreateToken())
    



class XAuthVerify(MainAPIView):
    def post(self, request:Request):
        USER_MODEL = get_user_model()
        request_data = XAuthForm(request.data)
        if not request_data.is_valid():
            raise exceptions.ValidationError({"detail": "Data Not Valid"})
        
        mfaToken = request_data.cleaned_data['mfaToken']
        code = request_data.cleaned_data['code']

        ic(get_user_model().userByJwt(mfaToken))
        
        return Response()

