# -*- coding: utf-8 -*-
import re

from django.forms import ModelForm
from django.forms import forms

from operations.models import UserQuestion


class UserRequestForm(ModelForm):

    class Meta:
        model = UserQuestion
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        res = re.compile("\d{10}")
        if res.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('Invalid Mobile', 'invalid_mobile')
