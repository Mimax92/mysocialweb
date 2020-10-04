from .models import Gossip
from django import forms
from django.forms import ModelForm



class GossipForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label='Gossip')
    photo = forms.ImageField(label='Photo', required=False)
    title = forms.CharField(max_length=25)