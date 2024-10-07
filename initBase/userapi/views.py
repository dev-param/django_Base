from django.contrib.auth import authenticate

# drf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions

import json
# locals
from .forms import LoginForm
from .task import sendmailOtp
from initBase.celery import debug_task
from .auth.tokenManager import TokenManager
# Create your views here.




class MainAPIView(APIView):
    def parseError(self, exceptionClass, strDetails="Something Wrong", jsonDetails={}):
        return exceptionClass({
            "detail": strDetails,
            "JsonInfo": json.loads(str(jsonDetails))
        })

    


class LoginAPIView(MainAPIView):
    def post(self, request):
       
        
        formData = LoginForm(request.data)
  
        if not formData.is_valid():
            raise self.parseError(exceptions.ValidationError, "Username Or Password Not Valid !", formData.errors.as_json(escape_html=True))
        

        user = authenticate(request, username=formData.cleaned_data['username'], password=formData.cleaned_data['password'])
        if user is None:
            raise self.parseError(exceptions.ValidationError, "Username Or Password Not Valid !")
 
        
        
        ic(user.CreateToken())
        


        return Response()