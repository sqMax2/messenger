from django.db import models
from django.contrib.auth.models import User
from annoying.fields import AutoOneToOneField
from django.db.models import signals


# auto Member creation
def create_member(sender, instance, created, **kwargs):
    """Create ModelB for every new ModelA."""
    if created or (not hasattr(instance, 'member')):
        Member.objects.create(user=instance)


signals.post_save.connect(create_member, sender=User, weak=False,
                          dispatch_uid='models.create_member')


class GroupChat(models.Model):
    name = models.CharField(max_length=64, unique=True, help_text='Room name')
    # members = models.ManyToManyField(User, related_name='rooms')


class Member(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='uploads/')
