from django import forms
from django.core.exceptions import ValidationError
from qSite.models import Profile
# from qSite.models import *

class SignInForm(forms.Form):
  login = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'form-control','placeholder': 'Login'
  }))
  password = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'form-control','placeholder': 'Password'
  }))

  def clean_login(self):
    data = self.cleaned_data.get('login')
    if Profile.objects.filter(username=data).first() is None:
      raise ValidationError('Username does not exist.')
    else:
      return data;

class SignUpForm(forms.Form):
  login = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'form-control','placeholder': 'Login'
  }))
  email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
    'class': 'form-control','placeholder': 'Email'
  }))
  password1 = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'form-control','placeholder': 'Password'
  }))
  password2 = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'form-control','placeholder': 'Confirm password'
  }))
  avatar = forms.FileField(required=False)

  def clean_login(self):
    data = self.cleaned_data.get('login')
    if Profile.objects.filter(username=data).first() is None:
      return data
    else:
      raise ValidationError('Username already exists.')

  def clean_email(self):
    data = self.cleaned_data.get('email')
    if data:
      if Profile.objects.filter(email=data).first() is None:
        return data
      else:
        raise ValidationError('Email already exists.')
    else:
      return data

  def clean_password2(self):
    pass1 = self.cleaned_data.get('password1')
    pass2 = self.cleaned_data.get('password2')
    if pass1 and pass2:
      if pass2 != pass1:
        self.add_error(None, 'Passwords did not match.')
      else:
        return pass2

  # class Meta:
  #   model = Profile
  #   fields = ('username', 'password1', 'password2', 'avatar', 'email')
  #   widgets = {
  #     'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Login'}),
  #     'password1': forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password'}),
  #     'password2': forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Confirm password'}),
  #     'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email'}),
  #   }
