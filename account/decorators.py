from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test,login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import CustomUser, UserProfile

def is_tenant(self):
    if str(self.user_type) == 'Tenant':
        return True
    else:
        return False
tenant_required = user_passes_test(
    lambda u: True if u.is_tenant 
    else False, 
    login_url='/')


def is_tenant(self):
    if str(self.user_type) == 'Landlord':
        return True
    else:
        return False
landlord_required = user_passes_test(
    lambda u: True if u.is_landlord
    else False, 
    login_url='/')
