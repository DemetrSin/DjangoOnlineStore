from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import Client, Review


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']


class ClientCreateForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ['first_name', 'surname', 'phone', 'delivery_address']


class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'surname', 'phone', 'delivery_address', 'email']


class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['grade', 'review_text']
