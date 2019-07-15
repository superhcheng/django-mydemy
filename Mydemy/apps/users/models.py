from __future__ import unicode_literals
from datetime import datetime

from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models



class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=30, verbose_name='Nick Name')
    birthday = models.DateField(verbose_name='Birthday', null=True, blank=True)
    sex = models.CharField(max_length=10, choices=(('M','Male'), ('F', 'Female')), default='M', verbose_name='Sex')
    address = models.CharField(max_length=100, default='', verbose_name="Address")
    mobile = models.CharField(max_length=10, verbose_name='Mobile Number', null=True, blank=True)
    image = models.ImageField(upload_to='image/users/profile/%Y/%m', default='image/users/profile/default.png', verbose_name='Profile Picture')

    class Meta:
        verbose_name = 'User Information'
        verbose_name_plural = verbose_name


class UserProfileVerification(models.Model):
    code = models.CharField(max_length=50, verbose_name='User Profile Verification Code')
    email = models.EmailField(max_length=100, verbose_name='E-mail')
    type = models.CharField(max_length=20, choices=(('register', 'Register'), ('reset','Reset Password')), verbose_name='Verification Type')
    verify_time = models.DateTimeField(default=timezone.now, verbose_name='Verification Time')

    class Meta:
        verbose_name = 'User Profile Verification'
        verbose_name_plural = 'User Profile Verifications'


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name='Banner Title')
    image = models.ImageField(upload_to='image/users/banner/%Y/%m', default='image/users/banner/default.png', verbose_name='Banner Picture')
    url = models.URLField(max_length=200, verbose_name='Banner URL')
    idx = models.IntegerField(default=100, verbose_name='Index')
    create_time = models.DateTimeField(default=datetime.now, verbose_name="Banner Creation Time")

    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'