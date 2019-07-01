# -*- coding: utf-8 -*-

from django.forms import ModelForm

from operations.models import UserQuestion


class UserRequestForm(ModelForm):
    class Meta:
        model = UserQuestion
        fields = ['name', 'mobile', 'course_name']