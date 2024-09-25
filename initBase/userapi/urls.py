
from django.urls import path
from .views import LoginAPiView
loginurlpatterns = [
    path('login/', LoginAPiView.as_view()),
]
