from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/users/online/', consumers.UserConsumer.as_asgi()),
    re_path(r'ws/communication/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/celery/', consumers.CeleryConsumer.as_asgi()),
]
