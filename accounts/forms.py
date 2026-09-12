from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Customer, Seller

class UserRegisterForm(UserCreationForm):
    
    role = forms.ChoiceField(choices=[
        ('customer', 'Customer'),
        ('seller', 'Seller')
    ], widget=forms.RadioSelect)
    
    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name', 'password1', 'password2']
        

class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ['phone']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=20, label='نام کاربری')
    password = forms.CharField(widget=forms.PasswordInput, label='رمز عبور')
    