from django.urls import path, include
from rest_framework.routers import DefaultRouter

from userManagement import views

# Create a router and register our ViewSets with it.
# router = DefaultRouter()
# router.register(r'create/', views.CreateUserApiView, basename='user-create')
# router.register(r'users', views.UserViewSet, basename='user')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('create/', views.CreateUserApiView.as_view(), name="user-create"),
    path('login/', views.LoginUserApiView.as_view(), name="user-login"),
    path('profile/', views.ProfileApi.as_view(), name="user-profile"),
]