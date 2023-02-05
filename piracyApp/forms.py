from django import forms
from .models import *
from .models import CustomLogin, Customer
import socket
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import django.contrib.auth.password_validation as validators
from django.core.validators import validate_ipv46_address, RegexValidator
from ipware.ip import get_client_ip
from django_cryptography.fields import encrypt
from django.contrib.auth.hashers import PBKDF2PasswordHasher,make_password


validate_hostname = RegexValidator(regex=r'[a-zA-Z0-9-_]*\.[a-zA-Z]{2,6}')

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField()

    class Meta:
        model = Customer
        fields = [ 'username']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None) # Now you use self.request to access request object.
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data['password1']
        validators(password)
        return password


    def is_valid_ipv4_address(address):
        try:
            socket.inet_pton(socket.AF_INET, address)
        except AttributeError:  # no inet_pton here, sorry
            try:
                socket.inet_aton(address)
            except socket.error:
                return print('Not a valid address')
            return address.count('.') == 3
        except socket.error:  # not a valid address
            return print('Not a valid address')

        return True

    def is_valid_ipv6_address(address):
        try:
            socket.inet_pton(socket.AF_INET6, address)
        except socket.error:  # not a valid address
            return print("Not a valid IP address")
        return True
    
    def clean_email(self):
        data = self.cleaned_data['email']
        duplicate_users = Customer.objects.filter(email=data)
        if self.instance.pk is not None:  # If you're editing an user, remove him from the duplicated results
            duplicate_users = duplicate_users.exclude(pk=self.instance.pk)
        if duplicate_users.exists():
            raise forms.ValidationError("E-mail is already registered!")
        return data
    
    def clean_username(self):
        data = self.cleaned_data['username']
        return data
    

class EditFileForm(forms.ModelForm):

    description= forms.CharField(widget=forms.Textarea)  

    class Meta:
        model = File
        fields = ['sourceFile', 'title', 'description']

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser():
            kwargs['form'] = EditFileForm
        else:
            kwargs['form'] = UserRegistrationForm
        return super(self).get_form(request,obj=obj,**kwargs)

    def __str__(self):
        return self.description
    
    def clean_username(self):
        data = self.cleaned_data['description']
        return data

class CreateForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['sourceFile', 'title', 'description']

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser():
            kwargs['form'] = CreateForm
        else:
            kwargs['form'] = UserRegistrationForm
        return super(self).get_form(request,obj=obj,**kwargs)

    def __str__(self):
        return self.title

class LoginForm(AuthenticationForm):

    serial_key = forms.UUIDField(label = "Serial Key",max_length = 120, required = True)

    class Meta:
        model = Customer
        fields =['serial_key']
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
    
    def clean_serial_Key(self, request, obj = None, **kwargs):
        serial_key = self.cleaned_data['serial_key']
        duplicate_key = File.objects.filter(key=serial_key)
        if self.instance.pk is not None:  # remove duplicated key
            duplicate_key = duplicate_key.exclude(pk=self.instance.pk)
        if duplicate_key.exists():
                raise forms.ValidationError("Key is already taken!")
        if serial_key:
            return super(self).get_form(request,obj=obj,**kwargs)

    def save(self, commit=True):
        user = super(LoginForm, self).save(commit=False)
        user.serial_key = self.cleaned_data["serial_key"]
        if commit:
            user.save()
        return user