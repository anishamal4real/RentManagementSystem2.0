from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class RegistrationForm(UserCreationForm):
    # email = forms.EmailField(required=True)
    class Meta:
        model = CustomUser
        fields = (
        'username',
        'name',
        'email',
        'user_type',
        'phone_number',
        'password1',
        'password2'
    )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.name = self.cleaned_data['name']
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):
    template_name= '/something/else'

    class Meta:
        model= CustomUser
        fields= (
            'email',
            'username',
            'name',
            'user_type',
            
        )
