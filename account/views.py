from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from .serializers import CustomUserSerializer, TenantSerializer, LandlordSerializer, RentSerializer
from django.views.decorators.csrf import csrf_exempt
from .models import Tenant, Landlord, Rent
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from .models import CustomUser
from  account.forms import RegistrationForm,EditProfileForm, EditTenantForm, EditLandlordForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test,login_required
from .decorators import landlord_required,tenant_required
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class=CustomUserSerializer
    queryset= CustomUser.objects.all()

class TenantViewSet(viewsets.ModelViewSet):
    serializer_class= TenantSerializer
    queryset= Tenant.objects.all()


class LandlordViewSet(viewsets.ModelViewSet):
    serializer_class= LandlordSerializer
    queryset= Landlord.objects.all()


class RentViewSet(viewsets.ModelViewSet):
    serializer_class= RentSerializer
    queryset= Rent.objects.all()

def home(request):
    return HttpResponse('This is the home page.')
def tenant(request):
    return HttpResponse('This is the page for the tenants.')
def landlord(request):
    return HttpResponse('This is the page for the landlords.')




# Create your views here.
@login_required
def home(request):
    return render(request, 'account/dashboard.html')

@login_required
def tenant(request, pk_test):
	tenants = Tenant.objects.filter(id=pk_test)
	return render(request, 'account/tenant.html',{'tenants': tenants})


def landlord(request, pk):
	landlords = Landlord.objects.filter(id=pk)
	return render(request,'account/landlord.html',{'landlords':landlords})

def rent(request, pk):
	rents= Rent.objects.filter(id=pk)
	return render (request, 'account/rent.html',{'rents':rents})

@csrf_exempt
def registerPage(request):
	form= RegistrationForm()
	if request.method=='POST':
		form= RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	context={'form':form}
	return render(request,'account/register.html',context)

@csrf_exempt
def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request,user)
				return redirect('home')
			else:
				messages.info(request, 'Username Or password is incorrect')
		context={}
		return render(request, 'account/login.html',context)
    
def logoutUser(request):
	logout(request)
	return redirect('login')
'''
@csrf_exempt
def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'account/reg_form.html', args)
        '''
@login_required
def view_profile(request, pk=None):
    if pk:
        user = CustomUser.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'account/profile.html', args)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view_profile'))
            #GET
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'account/edit_profile.html', args)

@login_required
@tenant_required 
def view_tenant(request):
    if request.method=='POST':
        if id:
             tenant = Tenant.objects.get(pk=id)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'account/tenantinfo.html', args) 

@login_required
@tenant_required
def edit_tenant(request):
    if request.method == 'POST':
        form =EditTenantForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view_tenant'))
            
    else:
        form = EditTenantForm(instance=request.tuser)
        args = {'form': form}
        return render(request, 'account/edit_tenant.html', args)

@login_required
@landlord_required
def view_landlord(request):
    if request.method=='POST':
        if id:
             landlord = Landlord.objects.get(pk=id)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'account/landlordinfo.html', args) 

@login_required
@landlord_required
def edit_landlord(request):
    if request.method == 'POST':
        form =EditLandlordForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view_landlord'))
            #GET
    else:
        form = EditLandlordForm(instance=request.user)
        args = {'form': form}
        return render(request, 'account/edit_landlord.html', args)



