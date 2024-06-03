# chat/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from core.models import ChatRoom, ChatRoomUser
from account.decorators import check_profile_complete
from django.contrib.auth.models import User

def get_one_to_one_group_name(user1, user2):
    # Combine usernames to create a unique group name
    sorted_user_ids = sorted([user1, user2])
    room_identifier = '-'.join(str(user_id) for user_id in sorted_user_ids)
    return room_identifier

@login_required
@check_profile_complete
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
def create_one_to_one_chat_room(request, username):
    user2 = get_object_or_404(User, username=username)
    name = get_one_to_one_group_name(request.user.username,user2.username)
    room = ChatRoom.objects.filter(name=name, is_group=False).first()
    if not room:
        room = ChatRoom.objects.create(name=name, created_by=request.user, is_group=False)
        ChatRoomUser.objects.create(user=request.user, chatroom=room)
        ChatRoomUser.objects.create(user=user2, chatroom=room)
    return redirect('chat_room', room_id=room.id)

@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom.objects.filter(deleted_at__isnull=True), id=room_id)
    messages = room.messages.filter(deleted_at__isnull=True).order_by('created_at')
    participants = room.chatroomuser_set.all()
    return render(request, 'chat/rooms.html', {'room': room, 'chat_messages': messages, 'participants': participants})

def get_one_to_one_group_name(user1, user2):
    # Combine usernames to create a unique group name
    sorted_user_ids = sorted([user1, user2])
    room_identifier = '-'.join(str(user_id) for user_id in sorted_user_ids)
    return room_identifier
