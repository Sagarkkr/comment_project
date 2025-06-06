"""
URL configuration for comment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from user_auth.login import obtain_auth_token

schema_view = get_schema_view(
    openapi.Info(
        title="Comment handle",
        default_version='v1',
        description="Welcome to the world of AI inspection of comments",
        terms_of_service="",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api-claim/api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('auth/v1/', include('user_auth.urls')),
    path('comment/v1', include('comment_handle.urls'))
]
