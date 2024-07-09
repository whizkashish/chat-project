from django.urls import path
from .api_views import ChatRoomList, MessageList, ChatRoomUsers

urlpatterns = [
    path('chatrooms/', ChatRoomList.as_view(), name='chatroom-list'),
    path('chatroomusers/', ChatRoomUsers.as_view(), name='chatroom-users'),
    path('chatrooms/<uuid:room_id>/messages/', MessageList.as_view(), name='message-list'),
]
