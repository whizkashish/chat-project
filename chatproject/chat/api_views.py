# chat/views.py
from core.models import ChatRoom, ChatRoomUser, Message
from django.contrib.auth.models import User
from rest_framework import generics, permissions, authentication
from .serializers import MessageSerializer, ChatRoomSerializer, ChatRoomUserSerializer

class ChatRoomList(generics.ListCreateAPIView):
    serializer_class = ChatRoomUserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatRoomUser.objects.filter(user=self.request.user,chatroom__is_group = True) #User.objects.exclude(id=self.user.id).exclude(is_superuser=True, is_staff=True)

class ChatRoomUsers(generics.ListCreateAPIView):
    
    serializer_class = ChatRoomUserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.exclude(id=self.user.id).exclude(is_superuser=True, is_staff=True)

class MessageList(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return Message.objects.filter(room_id=room_id).order_by('id')
