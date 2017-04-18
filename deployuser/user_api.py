#coding: utf-8
from .models import CustomUser


def auth_user(username=None, password=None):
    try:
        user = CustomUser.objects.get(username=username)
        if user.check_password(password):
            return user
    except CustomUser.DoesNotExist:
        return None
