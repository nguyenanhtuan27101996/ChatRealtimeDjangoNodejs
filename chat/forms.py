from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError,ObjectDoesNotExist
import re

class RegistationForm(forms.Form):
    username = forms.CharField(max_length=30,widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username',

        }
    ))
    email = forms.EmailField(required=True,widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email',

        }
    ))
    first_name = forms.CharField(max_length=30,widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'First name',

        }
    ))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Last name',

        }
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',

        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',

        }
    ))

    #check password confirm equal password
    def clean_password2(self):
        if 'password1' in self.data:
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')
            if password1 and password2 and password1 ==password2:
                return password2
        raise ValidationError('Password does not match the confirm password.')

    #check if username  existed
    def clean_username(self):
        if 'username' in self.data:
            username = self.cleaned_data.get('username')
            if not re.search(r'^\w+$',username):
                raise ValidationError('Username can not contain special characters.')
            try:
                User.objects.get(username=username)
            except ObjectDoesNotExist:
                return username
            raise ValidationError('Username have already existed.')

    #create user
    def save(self):
        User.objects.create_user(self.cleaned_data['username'],
                                 self.cleaned_data['email'],
                                 self.cleaned_data['password1'],
                                 first_name=self.cleaned_data['first_name'],
                                 last_name=self.cleaned_data['last_name'])


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'name': 'username',
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'name': 'password',

        }
    ))