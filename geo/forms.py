from django import forms
from geo.models import FeatureTypes, Locus, Language, Heritage

feature_types = FeatureTypes.objects.all()
loci = Locus.objects.all()
languages = Language.objects.all()
heritage = Heritage.objects.all()


class LoginForm(forms.Form):
    username = forms.CharField(label="Your name", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


class NewRecordForm(forms.Form):
    descriptor = forms.CharField(label="Descriptor", max_length=200)
    feature_types = forms.ModelMultipleChoiceField(
        label="Feature types", queryset=feature_types
    )
    notes = forms.CharField(max_length=500)
    point = forms.CharField(max_length=500, widget=forms.HiddenInput())


class LocationSelection(forms.Form):
    locations = forms.ModelMultipleChoiceField(
        label="Select related locations:", queryset=loci
    )


class FeatureSelection(forms.Form):
    features = forms.ModelMultipleChoiceField(
        label="Select feature types:", queryset=feature_types
    )


class VariantAdd(forms.Form):
    variant_name = forms.CharField(label="Variant name")
    language = forms.ModelChoiceField(
        label="Language", queryset=languages, required=False
    )
    attestation = forms.CharField(label="Optional attestation", required=False)


class UrlAdd(forms.Form):
    uri = forms.URLField(label="URI")
    provenance = forms.ModelChoiceField(
        label="Optional provenance", queryset=heritage, required=False
    )
