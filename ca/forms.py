from django.contrib.auth.models import User
from django import forms
from ca.models import Poster, CAProfile, year_choices

year_choices_empty = [('','Year ')] + year_choices

class ImageUploadForm(forms.ModelForm):
    poster = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Poster
        fields = ['poster']

class CARegistrationForm(forms.ModelForm):

    name = forms.CharField(label="Name",
                               widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Name',}))

    email = forms.EmailField(label="Email",widget=forms.TextInput(attrs={'class':'form-control',
                                                                         'required':'true','placeholder':'Email'}))

    password1 = forms.CharField(label="Password",
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                'required':'true','type':'password', 'placeholder':'Password', 'name': 'password1'}))

    password2 = forms.CharField(label="Password",
                               widget=forms.TextInput(attrs={'class': 'form-control',
                               'required':'true','type':'password', 'placeholder':'Password (again)', 'name': 'password2'}))

    class Meta:
        model = User
        fields = ['name','email','password1','password2']
        exclude = ['username','first_name','last_name']

class ProfileCreationForm(forms.ModelForm):


    year = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'placeholder':'Year', }),choices=year_choices,)

    # college = forms.CharField(label="College",
    #                            widget=forms.TextInput(attrs={'class': 'form-control','type':'text', 'placeholder':"College"}))

    mobile_number = forms.IntegerField(label="Mobile Number",
                               widget=forms.TextInput(attrs={'class': 'form-control','type':'text', 'placeholder':"Mobile Number"}))

    whatsapp_number = forms.IntegerField(label="WhatsApp Number",
                               widget=forms.TextInput(attrs={'class': 'form-control','type':'text', 'placeholder':"WhatsApp Number"}))

    college_address = forms.CharField(label="College Address",
                               widget=forms.Textarea(attrs={'class': 'form-control','type':'textarea', 'rows': '5','placeholder':"College Address"}))

    postal_address = forms.CharField(label="Postal Address",
                               widget=forms.Textarea(attrs={'class': 'form-control','type':'textarea','rows': '5', 'placeholder':"Postal Address"}))


    class Meta:
        model = CAProfile
        fields = ['year','mobile_number','whatsapp_number','college_address','postal_address']
        exclude = ['user_id','user','profile_photo','college']

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
