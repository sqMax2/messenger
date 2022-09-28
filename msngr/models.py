from django.db import models
from django.contrib.auth.models import User


class GroupChat(models.Model):
    name = models.CharField(max_length=64, unique=True, help_text='Room name')
    # members = models.ManyToManyField(User, related_name='rooms')


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='uploads/')
