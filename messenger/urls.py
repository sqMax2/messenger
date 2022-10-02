"""messenger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from msngr.views import UserViewset, RoomViewset, MemberViewset
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings


# REST
router = routers.DefaultRouter()
router.register(r'room', RoomViewset)
router.register(r'user', UserViewset)
router.register(r'member', MemberViewset)


urlpatterns = [
    path('chat/', include('msngr.urls')),
    path('admin/', admin.site.urls),
    path('', include('protect.urls')),
    path('sign/', include('authapp.urls')),
    path('accounts/', include('allauth.urls')),
    path('logout/', LogoutView.as_view()),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
