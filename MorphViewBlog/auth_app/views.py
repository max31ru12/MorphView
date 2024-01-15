import os
import sys

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, LoginView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.core.mail import send_mail

from .forms import UserCreationForm, CustomSetPasswordForm

sys.path.append(os.path.join(os.getcwd(), '..'))
from utils import DataMixin


# Create your views here.
class Register(DataMixin, View):
    template_name = "registration/Register.html"

    def get(self, request):
        context = {
            "form": UserCreationForm(),
            "title": super().get_user_context(title='Регистрация')['title']
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('base')
        context = {
            "form": form,
        }

        return render(request, self.template_name, context)


class Logout(DataMixin, View):

    def get(self, request):
        logout(request)
        return redirect('base')


class LoginView(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path_list = self.request.META.get('HTTP_REFERER', '/').split('/')
        if 'auth' not in path_list and 'login' not in path_list:
            context['previous_path'] = self.request.META.get('HTTP_REFERER', '/')
        return context


class CustomPasswordResetView(DataMixin, PasswordResetView):
    template_name = 'password_reset/password_reset_form.html'
    email_template_name = 'password_reset/password_reset_email.html'
    subject_template_name = "password_reset/password_reset_email.html"
    success_url = reverse_lazy("auth_app:password_reset_done")


class CustomPasswordResetDoneView(DataMixin, PasswordResetDoneView):
    template_name = 'password_reset/password_reset_done.html'


class CustomPasswordResetConfirmView(DataMixin, PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("auth_app:password_reset_complete")
    template_name = "password_reset/password_reset_confirm.html"


class CustomPasswordResetCompleteView(DataMixin, PasswordResetCompleteView):
    template_name = "password_reset/password_reset_complete.html"
