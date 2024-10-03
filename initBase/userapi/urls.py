
from django.urls import path
from .views import LoginAPIView
loginurlpatterns = [
    path('login/', LoginAPIView.as_view()),
]
