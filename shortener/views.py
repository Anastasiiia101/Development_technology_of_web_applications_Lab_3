import urllib
import requests

from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic.edit import FormView

from . import models
from . import serializers
from .forms import SendEmailForm
from .tasks import send_url_dump
from .permissions import IsOwnerOrReadOnly

from settings import CUTTLY_API_KEY


User = get_user_model()


class Home(APIView):
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        return Response('Index page of xLink application')


def get_short_url(original_url):
    url = urllib.parse.quote(original_url)
    r = requests.get(
        'http://cutt.ly/api/api.php?key={}&short={}'.format(CUTTLY_API_KEY, url)
    )
    res = r.json()['url']
    return res['title'], res['shortLink']


class URLList(generics.ListCreateAPIView):
    queryset = models.URL.objects.all()
    serializer_class = serializers.URLSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return models.URL.objects.filter(owner=user)

    def perform_create(self, serializer):
        original_url = self.request.POST['original_url']
        site_title, short_url = get_short_url(original_url)

        serializer.save(
            name=site_title,
            short_url=short_url,
            owner=self.request.user,
        )


class URLDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.URL.objects.all()
    serializer_class = serializers.URLSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        user = self.request.user
        return models.URL.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class About(APIView):
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        return Response(
            {
                'about': (
                    'xLink is a link shortener application. '
                    'Don`t let the links limit you.'
                )
            }
        )


class Profile(APIView):
    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({
            'username': request.user.username,
            'email': request.user.email,
            'gender': models.GENDER(request.user.gender).name,
            'birthday': request.user.birthday,
        })


class UserList(generics.ListAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer


class Communication(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, room_name, *args, **kwargs):
        return render(request, 'shortener/communication.html', {
            'room_name': room_name
        })


class StatusUserList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        users = User.objects.select_related('online_user')
        for user in users:
            user.status = 'Online' if hasattr(user, 'online_user') else 'Offline'
        return render(request, 'shortener/user_status.html', {'users': users})


class SendEmailView(FormView):
    template_name = 'shortener/contact.html'
    form_class = SendEmailForm
    success_url = '/'

    def form_valid(self, form):
        form.send_email()
        return super(SendEmailView, self).form_valid(form)


class UrlDumpView(APIView):
    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        send_url_dump.delay(
            request.user.id, request.user.username, request.user.email
        )
        return Response('URL dump sent')


class CeleryMonitor(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return render(request, 'shortener/monitor.html')
