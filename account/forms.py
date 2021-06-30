from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Landlord, Tenant, UserProfile
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class EditTenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['room_rent','electricity','house_no'] 
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active= True
        if commit:
           user.save()
        return user

class EditLandlordForm(forms.ModelForm):
    class Meta:
        model=Landlord
        fields=['house_no']
    def save(self,commit=True):
        user=super().save(commit=False)
        user.is_active=True
        if commit:
            user.save()
        return user

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
        'username',
        'name',
        'email',
        'user_type',
        'phone_number',
        'is_tenant',
        'password1',
        'password2',
        'is_landlord',
    )
    def save(self, commit=True):
        username = super().save(commit=False)
        username.is_active= True
        if commit:
            username.save()
        return username


class EditProfileForm(UserChangeForm):
    template_name= '/something/else'

    class Meta:
        model= CustomUser
        fields= (
            'email',
            'username',
            'name',
            
            
        )

