from django.http import JsonResponse
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required
from core.models import ChatRoom, ChatRoomUser, Profile, Notifications
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProfileUpdateForm, CustomUserCreationForm

@login_required
def account_view(request):
    user_chat_rooms = ChatRoomUser.objects.filter(user=request.user,chatroom__is_group = True)
    user_list = User.objects.exclude(id=request.user.id).exclude(is_superuser=True, is_staff=True)
    return render(request, 'account/account.html',{
        'user_chat_rooms': user_chat_rooms,
        'user_list' : user_list
    })

@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'account/public-profile.html', {'user': user})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/register.html', {'form': form})

@login_required
def notification_list(request):
    user_notifications = Notifications.objects.filter(user=request.user, is_read=False)
    notifications_data = [
        {
            'id' : notification.id,
            'message': notification.content,
            'link': f'/chat/chat_room/{notification.room.id}/',  # Adjust link based on your URL structure
            'icon': '/static/images/default-icon.png'  # Optional: add an icon field
        }
        for notification in user_notifications
    ]
    return JsonResponse({'notifications': notifications_data})

@login_required
@require_POST
def mark_as_read(request, notification_id):
    try:
        notification = Notifications.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notifications.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)
    

@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES , instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        profile_form = ProfileUpdateForm(instance=profile)
    return render(request, 'account/profile.html', {'profile_form': profile_form})

@login_required
def custom_logout_view(request):
    messages.success(request, 'Logged out Successfully')
    logout(request)
    return redirect('login')

