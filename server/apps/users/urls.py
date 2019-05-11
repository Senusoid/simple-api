from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from .views import CreateUserAPIView


urlpatterns = [
    path('create', CreateUserAPIView.as_view()),
    path('auth', obtain_jwt_token),
    path('refresh_token', refresh_jwt_token),
]
