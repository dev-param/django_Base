

# drf
from rest_framework.views import APIView
from rest_framework.response import Response
# locals
from .forms import LoginForm
# Create your views here.




class MainAPIView(APIView):
    pass


class LoginAPiView(MainAPIView):
    def post(self, request):
        formData = LoginForm(request)
        print(formData.get_user())
        print(formData.get_invalid_login_error())
        




        return Response({})