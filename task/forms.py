from django import forms
from task.models import *


class DirectorDetailForm(forms.ModelForm):

    class Meta:
        model = DirectorDetail
        exclude = ['ca']


class StudentBodyDetailForm(forms.ModelForm):

    class Meta:
        model = StudentBodyDetail
        exclude = ['ca']
