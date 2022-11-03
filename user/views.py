from django.views.generic import TemplateView, FormView
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.shortcuts import redirect

from . import forms


class LoginUserView(FormView):
    template_name = 'user/login.html'
    form_class = forms.LoginUserForm
    success_url = reverse_lazy('home:landing_page')

    def form_invalid(self, form):
        if form.errors.get('user_email'):
            return redirect(reverse_lazy('user:register'))
        return super().form_invalid(form)

    def form_valid(self, form):

        user = authenticate(self.request, email=form.cleaned_data['user_email'], password=form.cleaned_data['password'])

        if user:
            login(self.request, user)
            return super().form_valid(form)

        return super().form_valid(form)


class RegiserUserView(FormView):
    template_name = 'user/register.html'
    form_class = forms.ReigsterUserForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        new_user = form.create_new_user()
        return super().form_valid(form)
