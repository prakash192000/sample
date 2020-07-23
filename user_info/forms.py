from django import forms

from .models import UserProfileInfo

from django.contrib.auth.models import User

#user information form for details like name,password,email
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','email','password')

        
#user profile form for storing custom attributes
class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('date_of_birth' , 'phone' ,'passport_num' , 'profile_pic')