from django.views.generic import TemplateView, FormView
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.shortcuts import redirect

from . import forms
from home import models


class LoginUserView(FormView):
    template_name = 'user/login.html'
    form_class = forms.LoginUserForm
    success_url = reverse_lazy('home:landing_page')

    def form_invalid(self, form):
        if form.errors.get('user_email'):
            return redirect(reverse_lazy('user:register'))
        return super().form_invalid(form)

    def form_valid(self, form):
        user = get_user_model().objects.get(email=form.cleaned_data['user_email'])
        login(self.request, user)

        return super().form_valid(form)


class RegiserUserView(FormView):
    template_name = 'user/register.html'
    form_class = forms.ReigsterUserForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        new_user = form.create_new_user()
        return super().form_valid(form)


class UserLogoutView(TemplateView):
    template_name = ''

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('home:landing_page'))


class UserDetailView(TemplateView):
    template_name = 'user/detail.html'
    context_object_name = 'donation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user_model().objects.get(id=self.request.user.id)
        context['donations'] = models.Donation.objects.filter(user_id=user.id, is_taken=False)
        context['taken_donations'] = models.Donation.objects.filter(user_id=user.id, is_taken=True)
        return context


class UserDonationUpdateStatusView(TemplateView):
    template_name = ''

    def get(self, request, *args, **kwargs):
        donation = models.Donation.objects.get(id=kwargs.get('pk'))
        donation.is_taken = True
        donation.save()
        return redirect(reverse_lazy('user:detail'))


class UserChangePasswordView(FormView):
    template_name = 'user/change_password.html'
    form_class = forms.PasswordChangeForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        user = get_user_model().objects.get(id=self.request.user.id)

        if user.check_password(form.cleaned_data['old_password']):
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            return super().form_valid(form)

        form.add_error('old_password', 'Wrong password')
        return super().form_invalid(form)
