from django.contrib.auth.models import User
from django import forms
from ca.models import Poster

class ImageUploadForm(forms.ModelForm):
    poster = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Poster
        fields = ['poster']
