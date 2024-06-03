# myapp/decorators.py
from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

def check_profile_complete(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.profile.is_complete:  # Assuming your User model has a related Profile model
            messages.warning(request, 'Complete your profile first!')
            return redirect('/account/profile')  # Redirect to the profile completion page
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
