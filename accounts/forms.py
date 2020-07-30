from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import Order, Customer

class OrderForm(ModelForm):
    class Meta:
        # minimum 2 fields
        model = Order # get the fields
        fields ='__all__'  # write fields to form 


class CustomerForm(ModelForm):
    class Meta:
        # minimum2 fields
        model = Customer # get the fields
        fields ='__all__'  # write fields to form 

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']