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
    user_type = models.PositiveIntegerField(choices=ROLE_CHOICES, null=False)
    username= models.CharField(max_length=50, null=False,  unique=True)
    phone_number = models.CharField(max_length=14, null=False)
    is_active=models.BooleanField(default=True)
    
    
    
    def __str__(self):
        return self.username


class Tenant(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    house_no = models.CharField(max_length=200,null=True)
    room_rent = models.FloatField()
    electricity = models.FloatField()
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_tenant = models.BooleanField('Tenant', default=True)
    def __str__(self):
        return self.name


class Landlord(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=200, null=True)
    house_no = models.CharField(max_length=200, null=True)
    is_landlord = models.BooleanField('Landlord', default=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Rent(models.Model):
    tenant=models.ForeignKey(Tenant, null=True, on_delete=models.SET_NULL)
    landlord=models.ForeignKey(Landlord, null=True, on_delete=models.SET_NULL)
    date_created= models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return self.tenant.name or ''

class UserProfile(models.Model):   
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)
    @receiver(post_save, sender=CustomUser) 
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
    @receiver(post_save, sender=CustomUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
        




