from rest_framework import serializers
from core.models import Message, ChatRoom, ChatRoomUser

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id','content']

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'
class ChatRoomUserSerializer(serializers.ModelSerializer):
    chatroom = ChatRoomSerializer(read_only=True)
    class Meta:
        model = ChatRoomUser
        fields = '__all__'
