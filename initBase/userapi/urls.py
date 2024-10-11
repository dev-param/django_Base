
from django.urls import path
from .views import LoginAPIView, XAuthVerify
loginurlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('login/mfa/', XAuthVerify.as_view()),
    # path('profile/', ProfileAPIView.as_view()),
]
