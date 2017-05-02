#coding: utf-8
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import CustomUser
from rest_framework.authtoken.models import Token

def auth_user(username=None, password=None):
    try:
        user = CustomUser.objects.get(username=username)
        if user.check_password(password):
            return user
    except CustomUser.DoesNotExist:
        return None

# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
