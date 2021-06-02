"""url_shortener URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from shortener.views import Home, About

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

api1 = [
    path('shortener/', include('shortener.urls')),
    path('about/', About.as_view(), name='about'),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
]

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('api/v1/', include(api1)),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/v1/schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
]
