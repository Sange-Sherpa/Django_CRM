from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *

class OrderForm(ModelForm):
    class Meta:
        model   =  Order
        fields  =  '__all__'
        exclude = ['user']


class CustomerForm(ModelForm):
    class Meta:
        model   =  Customer
        fields  =  '__all__'


class CreateUserForm(UserCreationForm):
    email   =   models.EmailField()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'required': '',
            'name': 'username',
            'id': 'username',
            'type': 'text',
            'placeholder': 'username'
        })
        self.fields['email'].widget.attrs.update({
            'required': '',
            'name': 'email',
            'id': 'email',
            'type': 'email',
            'placeholder': 'email'
        })
        self.fields['password1'].widget.attrs.update({
            'required': True,
            'name': 'password1',
            'id': 'password1',
            'type': 'text',
            'placeholder': 'password'
        })
        self.fields['password2'].widget.attrs.update({
            'required': True,
            'name': 'password2',
            'id': 'password2',
            'type': 'text',
            'placeholder': 'confirm password'
        })
    class Meta:
        model   =   User
        fields  =   ['username', 'email', 'password1', 'password2']