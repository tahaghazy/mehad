from django import forms
from .models import *


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class UsercreationForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='يتكون من حروف وارقام فقط بدون مسافات', label='اسم المستخدم')
    first_name = forms.CharField(max_length=30, required=True, help_text='', label='الاسم الأول')
    last_name = forms.CharField(max_length=30, required=True, help_text='', label='الاسم الأخير')
    email = forms.EmailField(max_length=254,required=True, help_text='name@example.com',label='البريد الالكتروني')
    password1 = forms.CharField(max_length=30, required=True,label='كلمة المرور ', widget=forms.PasswordInput(), min_length=8)
    password2 = forms.CharField(max_length=30, required=True,help_text='قم بادخال كلمة المرور مره أخرى',label='تأكيد كلمة المرور', widget=forms.PasswordInput(), min_length=8)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('كلمة المرور غير متطابقه')
        return cd['password2']

    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('يوجد حساب باسم المستخدم هذا')
        return cd['username']


class LoginForm(forms.ModelForm):
    username = forms.CharField(label='اسم المستخدم ')
    password = forms.CharField(
        label='كلمة المرور', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')

class CheckoutForm(forms.ModelForm):

    class Meta:
        model = Orderr
        fields = ('full_name', 'phone','email', 'address',  'content')