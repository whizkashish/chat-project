from django.urls import path
from .api_views import ChatRoomList, MessageList

urlpatterns = [
    path('chatrooms/', ChatRoomList.as_view(), name='chatroom-list'),
    path('chatrooms/<int:chatroom_id>/messages/', MessageList.as_view(), name='message-list'),
]
