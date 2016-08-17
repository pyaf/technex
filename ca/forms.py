from django.contrib.auth.models import User
from django import forms
from ca.models import Poster

class ImageUploadForm(forms.ModelForm):
    poster_1 = forms.ImageField(widget = forms.ClearableFileInput)
    poster_2 = forms.ImageField(widget = forms.ClearableFileInput)
    poster_3 = forms.ImageField(widget = forms.ClearableFileInput)
    poster_4 = forms.ImageField(widget = forms.ClearableFileInput)

    class Meta:
        model = Poster
        fields = ['poster_1', 'poster_2', 'poster_3', 'poster_4']
