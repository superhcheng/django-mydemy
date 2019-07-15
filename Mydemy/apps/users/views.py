import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic.base import View

from .models import UserProfile, UserProfileVerification
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm, UpdateAvatarForm, EmailForm, UpdateEmailForm, UpdateUserProfileForm
from  utils.email_util import do_send_email
from utils.mixin_util import LoginMixInView


class CustomAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(mobile=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html',{})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'msg': 'Wrong Username or Password'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html', {'register_form': RegisterForm()})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')

            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html',{
                    'register_form': register_form,
                    'msg': 'This E-mail address has been taken'
                })
            user = UserProfile()
            user.username = email
            user.email = email
            user.password = make_password(password)
            user.is_active = False
            user.save()
            do_send_email(user.email, 'register')
            return render(request, 'login.html', {})
        else:
            return render(request, 'register.html', {'register_form': register_form, 'msg': 'Invalid input in the form'})


class ActivateView(View):
    def get(self, request, verification_code):
        user_verifications =  UserProfileVerification.objects.filter(code=verification_code)
        error_msg = ''
        if user_verifications:
            for user_verification in user_verifications:
                user = UserProfile.objects.get(email=user_verification.email)
                if user:
                    user.is_active = True
                    user.save()
                else:
                    error_msg = 'Exception --- not be able to find user'
        else:
            error_msg = 'Invalid activation link.'

        if len(error_msg) > 0:
            return render(request, 'verification_failed.html', {'error_msg': error_msg})
        return render(request, 'login.html')


class ForgetPwdView(View):
    def get(self, request):
        return render(request, 'forgetpwd.html', {'forget_pwd_form': ForgetPwdForm()})

    def post(self, request):
        forget_pwd_form = ForgetPwdForm(request.POST)
        if forget_pwd_form.is_valid():
            email = request.POST.get('email', '')
            do_send_email(email, 'reset')
            return render(request, 'forgetpwd_notification.html')
        else:
            return render(request, 'forgetpwd.html', {'error_msg': 'Invalid input in the form'})


class ResetPwdView(View):
    def get(self, request, verification_code):
        user_verifications =  UserProfileVerification.objects.filter(code=verification_code)
        for user_verification in user_verifications:
            user = UserProfile.objects.get(email=user_verification.email)
            if user:
                return render(request, 'forgetpwd_reset.html', {'email': user.email})
        return render(request, 'forgetpwd_reset_fail.html')


class DoResetPwdView(View):
    def post(self, request):
        reset_pwd_form = ResetPwdForm(request.POST)
        if reset_pwd_form.is_valid():
            pass1 = request.POST.get('password1', '')
            pass2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pass1 == pass2:
                user = UserProfile.objects.get(email=email)
                if user:
                    user.password = make_password(pass1)
                    user.save()
                else:
                    return render(request, 'forgetpwd_reset.html', {'error_msg': 'Invalid E-mail address'})
                return render(request, 'login.html')
            else:
                return render(request, 'forgetpwd_reset.html', {'error_msg' : 'Two passwords do not match'})
        else:
            return render(request, 'forgetpwd_reset.html', {'reset_pwd_form': reset_pwd_form})


class UserInfoView(LoginMixInView, View):
    def get(self, request):
        return render(request, 'user_info.html')


class UpdateUserAvatarView(LoginMixInView, View):
    def post(self, request):
        update_avatar_form = UpdateAvatarForm(request.POST, request.FILES, instance=request.user)
        if update_avatar_form.is_valid():
            update_avatar_form.save()
            return HttpResponse('{"status": "success", "msg": "Avatar update success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "err_msg": "Avatar update fail"}', content_type='application/json')


class UpdateUserPwdView(LoginMixInView, View):
    def post(self, request):
        reset_pwd_form = ResetPwdForm(request.POST)
        if reset_pwd_form.is_valid():
            pass1 = request.POST.get('password1', '')
            pass2 = request.POST.get('password2', '')
            if pass1 != pass2:
                return HttpResponse('{"status": "fail", "err_msg": "Passwords do not match!"}',content_type='application/json')
            else:
                request.user.password = make_password(pass2)
                request.user.save()
                return HttpResponse('{"status": "success", "msg": "Passwords updated"}',content_type='application/json')
        else:
            return HttpResponse(json.dumps(reset_pwd_form.errors), content_type='application/json')


class UpdateUserEmailGetVCView(LoginMixInView, View):
    def post(self, request):
        email_form = EmailForm(request.POST)
        if email_form.is_valid():
            email = email_form.cleaned_data.get('email')
            if UserProfile.objects.filter(email=email):
                return HttpResponse('{"status": "fail", "err_msg": "You cannot use this E-mail address."}',content_type='application/json')
            do_send_email(email, 'change_email')
            return HttpResponse('{"status": "success", "msg": "Verification code sent."}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(email_form.errors), content_type='application/json')


class UpdateUserEmailView(LoginMixInView, View):
    def post(self, request):
        update_email_from = UpdateEmailForm(request.POST)
        if update_email_from.is_valid():
            code = update_email_from.cleaned_data.get('code', '')
            email = update_email_from.cleaned_data.get('email', '')
            user_verification = UserProfileVerification.objects.filter(code=code, email=email)
            if user_verification:
                request.user.email = email
                user_verification.delete()
                request.user.save()
                return HttpResponse('{"status": "success", "msg": "Verification code sent."}', content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "err_msg": "Invalid verification code or E-mail"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(update_email_from.errors), content_type='application/json')


class UpdateUserProfileView(LoginMixInView, View):
    def post(self, request):
        user_profile_form = UpdateUserProfileForm(request.POST, instance=request.user)
        if user_profile_form.is_valid():
            user_profile_form.save()
            return HttpResponse('{"status": "success", "msg": "User profile updated"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_profile_form.errors), content_type='application/json')