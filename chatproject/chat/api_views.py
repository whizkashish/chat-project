# chat/views.py
from core.models import ChatRoom, ChatRoomUser, Message
from django.contrib.auth.models import User
from rest_framework import generics, permissions, authentication
from .serializers import MessageSerializer, ChatRoomSerializer

class ChatRoomList(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class MessageList(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chatroom_id = self.kwargs['chatroom_id']
        return Message.objects.filter(chatroom_id=chatroom_id).order_by('-timestamp')