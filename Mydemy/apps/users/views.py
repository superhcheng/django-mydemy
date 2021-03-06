import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from Mydemy.settings import PAGINATION_SETTINGS
from django.shortcuts import render_to_response

from .models import UserProfile, UserProfileVerification
from courses.models import Course
from organizations.models import CourseOrg, Instructor
from operations.models import UserFavorite, UserCourse, UserMessage
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm, UpdateAvatarForm, EmailForm, UpdateEmailForm, UpdateUserProfileForm
from utils.email_util import do_send_email
from utils.mixin_util import LoginMixInView


class CustomAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(mobile=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class HomeView(View):
    def get(self, request):
        on_sale_courses = Course.objects.filter(on_sale=True)[:3]
        courses = Course.objects.filter(on_sale=False)[:6]
        orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'on_sale_courses': on_sale_courses,
            'courses': courses,
            'orgs': orgs,
        })


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
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, 'login.html', {'msg': 'Wrong Username or Password'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class LogOutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('home'))


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


class UserFavCourseView(LoginMixInView, View):
    def get(self, request):
        user_fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=2)
        course_ids = [user_fav_course.fav_id for user_fav_course in user_fav_courses]
        return render(request, 'user_fav_course.html', {
            'courses': Course.objects.filter(id__in=course_ids),
        })


class UserFavInsView(LoginMixInView, View):
    def get(self, request):
        user_fav_instructors = UserFavorite.objects.filter(user=request.user, fav_type=1)
        ins_ids = [user_fav_instructor.fav_id for user_fav_instructor in user_fav_instructors]
        return render(request, 'user_fav_instructor.html', {
            'instructors': Instructor.objects.filter(id__in=ins_ids),
        })


class UserFavOrgView(LoginMixInView, View):
    def get(self, request):
        user_fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=3)
        org_ids = [org.fav_id for org in user_fav_orgs ]
        return render(request, 'user_fav_org.html', {
            'orgs': CourseOrg.objects.filter(id__in=org_ids)
        })


class UserCourseView(LoginMixInView, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        course_ids = [user_course.course.id for user_course in user_courses]
        return render(request, 'user_course.html', {
            'courses': Course.objects.filter(id__in=course_ids),
        })


class UserNotificationView(LoginMixInView, View):
    def get(self, request):
        type = request.GET.get('type', 'U')
        user_notifications = UserMessage.objects.filter(user=request.user, type=type)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(user_notifications, PAGINATION_SETTINGS['PAGE_RANGE_DISPLAYED'], request=request)
        user_notifications_ret = p.page(page)

        return render(request, 'user_notification.html', {
            'user_notifications': user_notifications_ret,
            'user_notification_type': type
        })


def handler404(request, *args, **argv):
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render_to_response('500.html')
    response.status_code = 500
    return response