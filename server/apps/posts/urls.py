from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


app_name = 'posts'

router = DefaultRouter()
router.register('', views.PostsViewSet, base_name='posts')

urlpatterns = [
    path('', include(router.urls))
]



