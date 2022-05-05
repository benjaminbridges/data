from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Profile


# if a new user is created it will also create a new profile
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='user')
        instance.groups.add(group)


# when a user is updated it will update the profile as well
@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if created == False:
        instance.profile.save()


# if a new user is created it will also create a new profile
@receiver(post_save, sender=Profile)
def create_profile(sender, instance, created, **kwargs):
    if created:
        User.objects.create(username=instance.email, email=instance.email, first_name=instance.first_name, last_name=instance.last_name)
