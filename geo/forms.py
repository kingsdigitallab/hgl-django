from django import forms
from geo.models import FeatureTypes,Locus

feature_types =  FeatureTypes.objects.all()
loci = Locus.objects.all()

class LoginForm(forms.Form):
    username = forms.CharField(label='Your name', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class NewRecordForm(forms.Form):
    descriptor = forms.CharField(label='Descriptor',max_length=200)
    feature_types = forms.ModelMultipleChoiceField(label='Feature types',\
        queryset=feature_types)
    notes = forms.CharField(max_length=500)
    point = forms.CharField(max_length=500,widget=forms.HiddenInput())


class LocationSelection(forms.Form):
	locations = forms.ModelMultipleChoiceField(label='Select related locations:',\
        queryset=loci)