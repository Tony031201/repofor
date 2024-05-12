from crispy_forms.bootstrap import InlineCheckboxes, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django import forms
from users.models import *

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta(UserCreationForm):
        model = User
        fields = ('username','email', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.field_class = 'mt-10'
        self.helper.layout = Layout(
            Field('image', css_class="single-input"),
            Field('birth_day', css_class="single-input"),
            Field('bio', css_class="single-input"),

            Field('email', css_class='single-input'),
            PrependedText('subscript', ''),
        )
        self.helper.add_input(Submit('submit', 'Update', css_class='primary-btn submit_btn'))

    class Meta:
        model = UserProfile
        widgets = {
            'birth_day':forms.DateInput(attrs={'type':'date'}),
            'subscript': forms.CheckboxInput(attrs={'class': 'styled-checkbox'}),
        }
        fields = (
            'image',
            'birth_day',
            'bio',

            'email',
            'subscript'
        )