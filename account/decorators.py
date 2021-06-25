from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test,login_required
from django.shortcuts import render


def is_tenant(self):
    if str(self.user_type) == 'Tenant':
        return True
    else:
        return False
tenant_required = user_passes_test(
    lambda u: True if u.is_tenant 
    else False, 
    login_url='/')

def tenant_login_required(view_func):
    decorated_view_func = login_required(tenant_required(view_func), login_url='/')
    return decorated_view_func


def is_landlord(self):
    if str(self.user_type) == 'Landlord':
        return True
    else:
        return False
landlord_required = user_passes_test(
    lambda u: True if u.is_tenant 
    else False, 
    login_url='/')

def landlord_login_required(view_func):
    decorated_view_func = login_required(landlord_required(view_func), login_url='/')
    return decorated_view_func

