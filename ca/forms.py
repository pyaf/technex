from django.contrib.auth.models import User
from django import forms
from ca.models import Poster,UserProfile

class ImageUploadForm(forms.ModelForm):
    poster = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Poster
        fields = ['poster']

class ProfileCreationForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ['user_id','user','profile_completed']
