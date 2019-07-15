# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm

from captcha.fields import CaptchaField

from .models import UserProfile, UserProfileVerification


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True, initial='')
    password = forms.CharField(required=True, min_length=6, initial='')
    captcha = CaptchaField(error_messages=dict(
        invalid = 'Incorrect Captcha',
    ))


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True, initial='')
    captcha = CaptchaField(error_messages=dict(
        invalid = 'Incorrect Captcha',
    ))


class ResetPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6, initial='')
    password2 = forms.CharField(required=True, min_length=6, initial='')


class UpdateAvatarForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class EmailForm(ModelForm):
    class Meta:
        model = UserProfileVerification
        fields = ['email']


class UpdateEmailForm(ModelForm):
    class Meta:
        model = UserProfileVerification
        fields = ['email', 'code']


class UpdateUserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nickname', 'birthday', 'sex', 'address', 'mobile']
