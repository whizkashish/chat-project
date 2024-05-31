from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from core.models import ChatRoom, ChatRoomUser, Profile
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProfileUpdateForm

@login_required
def account_view(request):
    user_chat_rooms = ChatRoomUser.objects.filter(user=request.user)
    return render(request, 'account/account.html',{
        'user_chat_rooms': user_chat_rooms
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'account/register.html', {'form': form})

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

