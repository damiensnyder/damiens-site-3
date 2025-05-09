from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from accounts.models import User
from content.views import get_theme


@csrf_exempt
def get_auth_token(request):
    if request.user.is_authenticated:
        token = AccessToken.for_user(request.user)
        token['username'] = request.user.username
        token['token_type'] = 'access'
        response = JsonResponse({
            'authenticated': True,
            'username': request.user.username
        })
        
        response.set_cookie(
            'auth_token', 
            str(token), 
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            domain='.ownsite.local' if settings.DEBUG else '.damiensnyder.com'
        )
    else:
        response = JsonResponse({'authenticated': False})
    
    # Set CORS headers
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Origin"] = (
        "http://arcade.ownsite.local:3000"
        if settings.DEBUG
        else "https://arcade.damiensnyder.com"
    )
    return response


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
