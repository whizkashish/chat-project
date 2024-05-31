# chat/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from core.models import ChatRoom, ChatRoomUser
from django.contrib.auth.models import User

@login_required
def create_group_chat_room(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        room = ChatRoom.objects.create(name=name, created_by=request.user, is_group=True)
        participants = request.POST.getlist('participants')
        for participant_id in participants:
            user = User.objects.get(id=participant_id)
            ChatRoomUser.objects.create(user=user, chatroom=room)
        ChatRoomUser.objects.create(user=request.user, chatroom=room)
        return redirect('chat_room', room_id=room.id)
    
    # Exclude current user and admin users
    users = User.objects.exclude(id=request.user.id).exclude(is_superuser=True, is_staff=True)
    return render(request, 'chat/create_group_room.html', {'users': users})

@login_required
def create_one_to_one_chat_room(request, user_id):
    user2 = get_object_or_404(User, id=user_id)
    room = ChatRoom.objects.create(created_by=request.user, is_group=False)
    ChatRoomUser.objects.create(user=request.user, chatroom=room)
    ChatRoomUser.objects.create(user=user2, chatroom=room)
    return redirect('chat_room', room_id=room.id)

@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom.objects.filter(deleted_at__isnull=True), id=room_id)
    messages = room.messages.filter(deleted_at__isnull=True).order_by('created_at')
    participants = room.chatroomuser_set.all()
    return render(request, 'chat/rooms.html', {'room': room, 'messages': messages, 'participants': participants})
