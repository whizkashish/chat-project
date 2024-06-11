from django.urls import path, re_path
from .consumers import ChatConsumer, ChartConsumer
ws_urlpatterns = [
        path(r'ws/home/', ChartConsumer.as_asgi()),
        re_path(r'ws/chat/(?P<room_id>[\w-]+)/$', ChatConsumer.as_asgi()),
        re_path(r'ws/chat/(?P<chatroom_name>[\w-]+)/$', ChatConsumer.as_asgi()),
    ]