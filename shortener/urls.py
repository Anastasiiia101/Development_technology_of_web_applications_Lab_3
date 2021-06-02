# api/urls.py
from django.urls import path
from functools import partial

from . import views

urlpatterns = [
    path('', views.URLList.as_view(), name='url-list'),
    path('<int:pk>/', views.URLDetail.as_view(), name='url-detail'),
    path('', views.UserList.as_view()),
    path('<int:pk>/', views.UserDetail.as_view(), name='user-details'),
    path('profile/', views.Profile.as_view(), name='user-profile'),
    path('communication/<str:room_name>/', views.Communication.as_view(), name='communication'),
    path('users/status/', views.StatusUserList.as_view(), name='user-status'),
    path('email', views.SendEmailView.as_view(), name='email'),
    path('dump', views.UrlDumpView.as_view(), name='report'),
    path('monitor', views.CeleryMonitor.as_view(), name='monitor'),
]
