from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile
from stackoverflow.common.mixins import BootstrapMixin


class UserForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class ProfileForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', )


class SignUpForm(BootstrapMixin, UserCreationForm ):
    avatar = forms.ImageField(required=False, label='Avatar')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'avatar')
