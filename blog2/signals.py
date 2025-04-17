from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile_blog2(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile_blog2(sender, instance, **kwargs):
    try:
        instance.blog2_profile.save()
    except Profile.DoesNotExist:
        pass
