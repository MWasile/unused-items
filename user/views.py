from django.shortcuts import render
from django.views.generic import TemplateView


class LoginUserView(TemplateView):
    template_name = 'user/login.html'


class RegiserUserView(TemplateView):
    template_name = 'user/register.html'
