from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from accounts.models import User
from content.views import get_theme


@permission_required('accounts.change_user', login_url='login')
def set_user_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        
        try:
            user = User.objects.get(username=username)
            user.password = make_password(new_password)
            user.save()
            messages.success(request, f"Password for {username} changed successfully.")
            return redirect('accounts:set_user_password')
        except User.DoesNotExist:
            messages.error(request, f"User {username} not found.")
    
    return render(request, 'accounts/set-user-password.html', {
        'theme': get_theme(request)
    })


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session to prevent the user from being logged out
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/set-own-password.html', {
        'form': form,
        'theme': get_theme(request)
    })
