from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from .views import CreateUserAPIView

app_name = 'users'

urlpatterns = [
    path('create', CreateUserAPIView.as_view(), name='signup'),
    path('auth', obtain_jwt_token, name='login'),
    path('refresh_token', refresh_jwt_token),
]
