from django.db import models
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

ADMIN = 1
STAFF = 2
TENANT = 3
LANDLORD = 4
ROLE_CHOICES = (
    (ADMIN, 'Super Admin'),
    (STAFF, 'Staff'),
    (TENANT, 'Tenant'),
    (LANDLORD, 'Landlord'))

class CustomUser(AbstractUser):
    REQUIRED_FIELDS = ['name', 'email', 'phone_number', 'user_type']
    USERNAME_FIELD = 'username'
    name=models.CharField(max_length=50, null=False)
    email=models.CharField(max_length=300, null=False)
    user_type = models.PositiveIntegerField(choices=ROLE_CHOICES, null=False)
    username= models.CharField(max_length=50, null=False,  unique=True)
    phone_number = models.CharField(max_length=14, null=False)
    is_active=models.BooleanField(default=True) 
    is_tenant = models.BooleanField(default=False)
    is_landlord = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
class UserProfile(models.Model):   
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="profile")
    
    def __str__(self):
        return str(self.user)

    def create_profile(sender, instance, created, *args, **kwargs):
    # ignore if this is an existing User
        if not created:
            return
        UserProfile.objects.create(user=instance)
    post_save.connect(create_profile, sender=CustomUser)

    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save(user=instance)
    post_save.connect(create_profile, sender=CustomUser)

    
     







class Tenant(models.Model):
    house_no = models.CharField(max_length=200,null=True)
    room_rent = models.FloatField()
    electricity = models.FloatField()
    is_tenant = models.BooleanField('Tenant', default=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.name or ''
    '''def create_tenant(sender, instance, created, *args, **kwargs):
    # ignore if this is an existing User
        if not created:
            return
        Tenant.objects.create(user=instance)
    post_save.connect(create_tenant, sender=CustomUser)

    def save_user_profile(sender, instance, **kwargs):
        instance.tenant_profile.save(user=instance)
    post_save.connect(create_tenant, sender=CustomUser)'''


class Landlord(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    house_no = models.CharField(max_length=200, null=True)
    is_landlord = models.BooleanField('Landlord', default=True)
    def __str__(self):
        return self.luser.name or ''
    '''def create_lprofile(sender, instance, created, *args, **kwargs):
    # ignore if this is an existing User
        if not created:
            return
        Landlord.objects.create(user=instance)
    post_save.connect(create_lprofile, sender=CustomUser)

    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save(user=instance)
    post_save.connect(create_lprofile, sender=CustomUser)'''


class Rent(models.Model):
    tenant=models.ForeignKey(Tenant, null=True, on_delete=models.SET_NULL)
    landlord=models.ForeignKey(Landlord, null=True, on_delete=models.SET_NULL)
    date_created= models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return self.tenant.name or ''

