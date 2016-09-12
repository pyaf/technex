from django import forms

class DirectorDetailForm(forms.ModelForm):

    class Meta:
        model = DirectorDetail
        exclude = ['dd','ca']


class DirectorDetailForm(forms.ModelForm):

    class Meta:
        model = studentBodyDetail
        exclude = ['sbd','ca']
