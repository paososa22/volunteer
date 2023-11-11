from django import forms 
from .models import ExtendedData,PreferredLanguage,Organization1,Comment,Interesados
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.forms import Textarea 



class AuthenticationUserForm(AuthenticationForm):
    class Meta:
        model=User
        fields = ['username','password']
        username = forms.CharField(max_length=30, required=True)
        password = forms.CharField(widget=forms.PasswordInput, required=True)


class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','password1','password2']
        def clean_password2(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')
            if password1 != password2:
                raise forms.ValidationError("Las contraseñas no coinciden.")
            return password2

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=ExtendedData
        fields ="__all__"
        
class UserLanguageForm(forms.ModelForm):
    class Meta:
        model=PreferredLanguage
        fields = "__all__"

class NuevaOrg1(forms.ModelForm):
    class Meta:
        model = Organization1
        fields = ['organization_name','organization_mail','organization_address','organization_web','organization_description','organization_type','volunteer_count']

class OrgSearchForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=False, label='Nombre')
    tipo = forms.ChoiceField(choices=[('', 'Sin selección')] +Organization1.TYPES_CHOICES, required=False, label='Tipo')
    interes = forms.BooleanField(required=False,label='Aun no te interesan')


class EditOrganization(forms.ModelForm):
    class Meta:
        model = Organization1
        fields = ['organization_web']

class EditNameOrganization(forms.ModelForm):
    class Meta:
        model = Organization1
        fields = [ 'organization_name']

class EditMailOrganization(forms.ModelForm):
    class Meta:
        model = Organization1
        fields = [ 'organization_mail']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class InteresaForm(forms.ModelForm):
    class Meta:
        model = Interesados
        fields = ['organizacion', 'user'] 
