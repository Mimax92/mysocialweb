from .models import Gossip
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model


class GossipForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label='Gossip', max_length=200)
    photo = forms.ImageField(label='Photo', required=False)
    title = forms.CharField(max_length=25)

class MessageForm(forms.Form):
    # def __init__(self, user, *args, **kwargs):
    #
    title = forms.CharField(max_length=35, label='Title')
    content = forms.CharField(widget=forms.Textarea, label='Content')
    receiver = forms.ModelChoiceField(queryset=User.objects.all(),
                              empty_label="Choose a receiver")

def validate_user(value):
    if get_user_model().objects.filter(username=value).exists():
        raise ValidationError('Username already exists')

class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=64, validators=[validate_user], label='Username')
    password = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Password')
    repeated_password = forms.CharField(max_length=32, widget=forms.PasswordInput, label='Repeat password')
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    email = forms.EmailField(validators=[EmailValidator()])


class Notiform(forms.Form):
    read = forms.BooleanField()


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label='comment', max_length=200)