from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from .serializers import TenantSerializer, LandlordSerializer, RentSerializer
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
from  account.forms import RegistrationForm,EditProfileForm
from django.db.models.signals import post_save
from django.dispatch import receiver
 


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

class TenantViewSet(viewsets.ModelViewSet):
    serializer_class= TenantSerializer
    queryset= Tenant.objects.all()


class LandlordViewSet(viewsets.ModelViewSet):
    serializer_class= LandlordSerializer
    queryset= Landlord.objects.all()


class RentViewSet(viewsets.ModelViewSet):
    serializer_class= RentSerializer
    queryset= Rent.objects.all()

'''
#For showcasing the details of Tenant
class TenantAPIView(APIView):
    def get(self,request):
        tenants= Tenant.objects.all()
        serializer=TenantSerializer(tenants, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=TenantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TenantDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Tenant.objects.get(id=pk)
        except Tenant.DoesNotExist:
            raise Http404("There is no such tenant.")

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = TenantSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        tenant = self.get_object(pk)
        serializer = TenantSerializer(tenant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tenant= self.get_object(pk)
        tenant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TenantListGenericAPIView(generics.ListCreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    lookup_field= 'id'
    #authentication_classes= [SessionAuthentication, BasicAuthentication]
    authentication_classes= [TokenAuthentication]
    permission_classes=[IsAuthenticated]


class TenantDetailGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

# For showcasing the details of the landlord
class LandlordAPIView(APIView):
    def get(self,request):
        tenants= Landlord.objects.all()
        serializer=LandlordSerializer(tenants, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=LandlordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LandlordDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Landlord.objects.get(id=pk)
        except Landlord.DoesNotExist:
            raise Http404("There is no such landlord.")

    def get(self, request, pk):
        landlord = self.get_object(pk)
        serializer = LandlordSerializer(landlord)
        return Response(serializer.data)

    def put(self, request, pk):
        landlord = self.get_object(pk)
        serializer = LandlordSerializer(landlord, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        landlord= self.get_object(pk)
        landlord.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LandlordListGenericAPIView(generics.ListCreateAPIView):
    queryset = Landlord.objects.all()
    serializer_class = LandlordSerializer
    lookup_field= 'id'
    #authentication_classes= [SessionAuthentication, BasicAuthentication]
    authentication_classes= [TokenAuthentication]
    permission_classes=[IsAuthenticated]


class LandlordDetailGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Landlord.objects.all()
    serializer_class = LandlordSerializer

class RentDetailGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer







'''
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


def create_profile(sender, instance, created, *args, **kwargs):
    # ignore if this is an existing User
    if not created:
        return
    CustomUser.objects.create(user=instance)
post_save.connect(create_profile, sender=CustomUser)