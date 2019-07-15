# -*- coding: utf-8 -*-

from random import Random

from django.core.mail import send_mail

from users.models import UserProfileVerification
from Mydemy.settings import EMAIL_HOST_USER


def do_send_email(email, send_type='register'):
    email_verification = UserProfileVerification()
    verification_code = generate_random_str(16)
    email_verification.code = verification_code
    email_verification.email = email
    email_verification.type = send_type
    email_verification.save()
    email_subject = ''
    email_body = ''
    if send_type == 'register':
        email_subject = 'Register Link'
        email_body = 'Click this link to register: http://127.0.0.1:8000/active/{0}'.format(verification_code)
    elif send_type == 'reset':
        email_subject = 'Reset Link'
        email_body = 'Click this link to reset: http://127.0.0.1:8000/resetpwd/{0}'.format(verification_code)
    elif send_type == 'change_email':
        email_subject = 'New E-mail Verification'
        email_body = 'Here your verification code {0}'.format(verification_code)
    else:
        print 'Exception Invalid Send Type... ' + send_type

    email_status = send_mail(email_subject, email_body, EMAIL_HOST_USER, [email])

    #print 'email_status', email_status
    if email_status:
        pass
    else:
        pass


def generate_random_str(string_len=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(string_len):
        str += chars[random.randint(0, length)]
    return str