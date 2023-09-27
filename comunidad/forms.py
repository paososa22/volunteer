from django import forms 
from .models import Organization1,ExtendedData,Comment,Interesados
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class AuthenticationUserForm(AuthenticationForm):
    class Meta:
        model=User
        fields = ['username','password']

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

class NuevaOrg1(forms.ModelForm):
    class Meta:
        model = Organization1
        fields = ['organization_name','organization_mail','organization_address','organization_web','organization_description','organization_type']

class OrgSearchForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=False, label='Nombre de la organización')
    tipo = forms.ChoiceField(choices=[('', 'Sin selección')] +Organization1.TYPES_CHOICES, required=False, label='Tipo de organización')

class EditOrganization(forms.ModelForm):
    class Meta:
        model = Organization1
        fields = [ 'organization_web']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class InteresaForm(forms.ModelForm):
    class Meta:
        model = Interesados
        fields = ['organizacion', 'user'] 
