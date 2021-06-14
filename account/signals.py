from RentManagementSystemAH.account.models import CustomUser
from .models import UserProfile, CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
def create_profile(sender, instance, created, *args, **kwargs):
    # ignore if this is an existing User
    if not created:
        return
    UserProfile.objects.create(user=instance)
post_save.connect(create_profile, sender=CustomUser)
@receiver(post_save, sender=CustomUser, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    username = instance
    if created:
        profile = UserProfile(user=instance)
        profile.save()