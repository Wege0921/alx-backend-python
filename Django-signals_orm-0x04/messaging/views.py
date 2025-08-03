from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Log out first
    user.delete()    # Trigger post_delete signal
    return redirect('home')  # Replace with your home or login page
