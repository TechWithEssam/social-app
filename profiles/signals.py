from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Profile, RelationshipFriends


def post_save_created_profile(sender, instance, created, **kwargs) :
    if created :
        Profile.objects.create(user=instance)
post_save.connect(post_save_created_profile, sender=User)

def post_save_add_friends(sender, instance, created, **kwargs) :
    sender = instance.sender
    receiver = instance.receiver
    if instance.status == "accepted" :
        sender.friends.add(receiver.user)
        receiver.friends.add(sender.user)
        sender.save()
        receiver.save()
post_save.connect(post_save_add_friends, sender=RelationshipFriends)


def pre_delete_from_friends(sender, instance, **kwargs) :
    sender = instance.sender
    receiver = instance.receiver
    sender.friends.remove(receiver.user)
    receiver.friends.remove(sender.user)
pre_delete.connect(pre_delete_from_friends, sender=RelationshipFriends)