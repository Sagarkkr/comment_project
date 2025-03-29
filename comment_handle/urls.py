from django.urls import path
from rest_framework.routers import DefaultRouter

#local imports
from comment_handle.views import CommentHandleViewset

comment_router = DefaultRouter()
comment_router.register('comment', CommentHandleViewset, basename='comment')

urlpatterns = [
]
urlpatterns = comment_router.urls + urlpatterns
