from django.contrib.auth.models import User
from django import forms
from ca.models import Poster, CAProfile, year_choices

year_choices_empty = [('','Year ')] + year_choices

class ImageUploadForm(forms.ModelForm):
    poster = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Poster
        fields = ['poster']

class ProfileCreationForm(forms.ModelForm):

    first_name = forms.CharField(label="First Name",
                               widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'First Name',}))

    last_name = forms.CharField(label="Last Name",
                               widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Last Name',}))

    year = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'placeholder':'Year', }),choices=year_choices,)

    college = forms.CharField(label="College",
                               widget=forms.TextInput(attrs={'class': 'form-control','type':'text', 'placeholder':"College"}))

    mobile_number = forms.IntegerField(label="Mobile Number",
                               widget=forms.TextInput(attrs={'class': 'form-control','type':'number', 'placeholder':"Mobile Number"}))

    whatsapp_number = forms.IntegerField(label="WhatsApp Number",
                               widget=forms.TextInput(attrs={'class': 'form-control','type':'number', 'placeholder':"WhatsApp Number"}))

    college_address = forms.CharField(label="College Address",
                               widget=forms.Textarea(attrs={'class': 'form-control','type':'textarea', 'rows': '5','placeholder':"College Address"}))

    postal_address = forms.CharField(label="Postal Address",
                               widget=forms.Textarea(attrs={'class': 'form-control','type':'textarea','rows': '5', 'placeholder':"Postal Address"}))

    pincode = forms.IntegerField(label="Pincode",
                               widget=forms.TextInput(attrs={'class': 'form-control','type':'number', 'placeholder':"Pincode"}))


    class Meta:
        model = CAProfile
        exclude = ['user_id','user','profile_completed']

# class ProfileCreationForm(forms.ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         super(ProfileCreationForm, self).__init__(*args, **kwargs)
#         for field_name in self.fields:
#             field = self.fields.get(field_name)
#             if field:
#                 if type(field.widget) in (forms.TextInput,forms.DateInput):
#                     field.widget = forms.TextInput(attrs={'placeholder': field.label})
#
#
#     class Meta:
#         model = UserProfile
#         exclude = ['user_id','user','profile_completed']
