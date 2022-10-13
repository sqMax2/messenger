'''
msngr Models
'''
from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals


# auto Member creation
def create_member(sender, instance, created, **kwargs):
    """Create ModelB for every new ModelA."""
    if created or (not hasattr(instance, 'member')):
        Member.objects.create(user=instance)


signals.post_save.connect(create_member, sender=User, weak=False,
                          dispatch_uid='models.create_member')


class Room(models.Model):
    name = models.CharField(max_length=64, unique=True, help_text='Room name')
    online = models.ManyToManyField(User, related_name='rooms')

    @property
    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return f'{self.name} ({self.get_online_count})'


class Member(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='uploads/')
