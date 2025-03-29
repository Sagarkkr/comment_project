from django.urls import path
from rest_framework.routers import DefaultRouter

#local imports
from user_auth.views import UserAuthViewset

auth_router = DefaultRouter()
auth_router.register('user', UserAuthViewset, basename='user')

urlpatterns = [
]
urlpatterns = auth_router.urls + urlpatterns
