from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

    class Meta:
        model = CustomUser
        fields = ("email", "phone_number", "first_name", "last_name", "gender")

    def __int__(self):
        self.fields['password1'].required = False
        self.fields['password2'].required = False
