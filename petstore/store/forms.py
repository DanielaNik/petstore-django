from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Delivery


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class RegistrationForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(BootstrapFormMixin, AuthenticationForm):
    class Meta:
        model = User

class DeliveryForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['address', 'city', 'country', 'number', 'email']