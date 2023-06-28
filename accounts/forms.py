from django.contrib.auth.forms import UserCreationForm
from .models import User


class CreateUser(UserCreationForm):
    password2 = None

    class Meta:
        model = User
        fields = ['username', 'password1']