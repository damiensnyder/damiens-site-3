from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


def set_user_password(request):
    if request.user.is_staff:
        if request.method == 'POST':
            user_id = request.POST.get('username')
            new_password = request.POST.get('password')
            change_password(user_id, new_password)
        return render(request, 'accounts/set-user-password.html')
    return render(request, 'content/illegal-hidden-access.html')


def change_password(user_id, new_password):
    user = User.objects.get(id=user_id)
    user.password = make_password(new_password)
    user.save()
    return user
