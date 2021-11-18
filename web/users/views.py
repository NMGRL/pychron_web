# ===============================================================================
# Copyright 2021 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
import os

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from users.forms import SignUpForm
from users.tokens import account_activation_token

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True

        user.save()
        login(request, user)
        return redirect(reverse('set_password'))
    else:
        return render(request, 'account_activation_invalid.html')


@login_required
def manage(request):
    if request.user.is_superuser:
        return render(request, 'manage.html')
    else:
        return render(request, 'no_permissions.html')


@login_required
def set_password(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SetPasswordForm(user)

    return render(request, 'set_password.html', {'form': form})


@login_required
def add_user(request):
    if request.user.is_superuser:
        message = ''

        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                # subject = 'Activate Your MySite Account'
                port = os.environ.get('DJANGO_HOST_PORT', ':1337')
                if port and not port.startswith(':'):
                    port = f':{port}'

                message = render_to_string('account_activation_email.html', {
                    'user': user,
                    'port': port,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                # user.email_user(subject, message)
        else:
            form = SignUpForm()

        return render(request, 'add_user.html', {'form': form, 'message': message})
    else:
        return render(request, 'no_permissions.html')


# @login_required
def signup(request):
    # if request.user.groups.first().name in ('manager',):
    #     if request.method == 'POST':
    #         form = SignUpForm(request.POST)
    #         if form.is_valid():
    #             user = form.save(commit=False)
    #             user.is_active = False
    #             user.save()
    #             current_site = get_current_site(request)
    #             subject = 'Activate Your MySite Account'
    #             message = render_to_string('account_activation_email.html', {
    #                 'user': user,
    #                 'domain': current_site.domain,
    #                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #                 'token': account_activation_token.make_token(user),
    #             })
    #             user.email_user(subject, message)
    #             return redirect('account_activation_sent')
    #     else:
    #         form = SignUpForm()
    #     return render(request, 'signup.html', {'form': form})
    # else:
    return render(request, 'contact_signup.html')


def dashboard(request):
    return render(request, "users/dashboard.html")
# ============= EOF =============================================
