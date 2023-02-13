
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.forms import ModelForm
from django import forms

class RegisterForm(UserCreationForm) :
    class Meta :
        model = User
        fields = [ 
            'username',
            'password1',
            'password2'
        ]

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['username'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"Username"})
        self.fields['password1'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"Password", "data-toggle":"password"})
        self.fields['password2'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"Password confirmation", 'data-toggle': 'password'})
   

class AuthenticationUserForm(AuthenticationForm) :
    class Meta :
        model = User
        fields = [ 
            "username",
            "password"
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password'].label = ''
        self.fields['username'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"username"})
        self.fields['password'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"Password"})


class ProfileForm(ModelForm) :
    class Meta :
        model = Profile
        fields = [ 
            "avatar",
            "bio",
            "gender",
            "country"
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].label = ''
        self.fields['bio'].label = ''
        self.fields['gender'].label = ''
        self.fields['country'].label = ''
        self.fields['bio'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"bio"})
        self.fields['gender'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"gender"})
        self.fields['country'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"Your Country"})


class UserForm(ModelForm) :
    class Meta :
        model = User
        fields = [ 
            "first_name",
            "last_name",
            "email",
            "username"
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = ''
        self.fields['last_name'].label = ''
        self.fields['email'].label = ''
        self.fields['username'].label = ''
        self.fields['username'].help_text = ''
        self.fields['first_name'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"first name"})
        self.fields['last_name'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"last name"})
        self.fields['email'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"Email"})
        self.fields['username'].widget.attrs.update({'class':"form-control","id":"exampleInputEmail1","placeholder":"username"})


