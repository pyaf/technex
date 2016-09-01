from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from TechnexUser.models import TechProfile
from ca.models import year_choices

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(label="first name",
                               widget=forms.TextInput(attrs={'class': 'form-control','required':'true','placeholder':'First Name',}))
    last_name = forms.CharField(label="last name",
                               widget=forms.TextInput(attrs={'class': 'form-control','required':'true','placeholder':'Last Name',}))

    email = forms.EmailField(label="Email",widget=forms.TextInput(attrs={'class':'form-control','required':'true','placeholder':'Email'}))

    password = forms.CharField(label="Password",
                               widget=forms.TextInput(attrs={'class': 'form-control','required':'true','type':'password', 'placeholder':'Password', 'name': 'password'}))

    year = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'required':'true','placeholder':'Year', }),choices=year_choices,)

    college = forms.CharField(label="College",
                               widget=forms.TextInput(attrs={'class': 'form-control','type':'text','required':'true', 'placeholder':"College"}))

    mobile_number = forms.IntegerField(label="Mobile Number",
                               widget=forms.TextInput(attrs={'class': 'form-control','type':'number', 'required':'true','placeholder':"Mobile Number"}))


    class Meta:
        model = TechProfile
        fields = ['first_name', 'last_name','email','password','year','college','mobile_number']
        exclude = ['user_id','user','profile_photo']


class LoginForm(forms.Form):
    email = forms.CharField(label="email", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Email','required':'true', 'name': 'email'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Password','required':'true', 'name': 'password'}))
