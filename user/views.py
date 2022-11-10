from django.views.generic import TemplateView, FormView, View
from django.contrib.auth import login, logout, get_user_model
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from . import forms
from . import tokens
from . import models
from home.models import Donation


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
        self.send_activation_email(new_user)
        return super().form_valid(form)

    def send_activation_email(self, user):
        token = tokens.token_generator.make_token(user)
        user.email_user(
            'Activate your account',
            f'Please click the link to activate your account: http://{self.request.get_host()}/user/activate/{user.pk}/{token}')


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('home:landing_page'))


class UserDetailView(TemplateView):
    template_name = 'user/detail.html'
    context_object_name = 'donation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user_model().objects.get(id=self.request.user.id)
        context['donations'] = Donation.objects.filter(user_id=user.id, is_taken=False)
        context['taken_donations'] = Donation.objects.filter(user_id=user.id, is_taken=True)
        return context


class UserDonationUpdateStatusView(View):
    def get(self, request, *args, **kwargs):
        donation = Donation.objects.get(id=kwargs.get('pk'))
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


class ActivateUserView(View):
    def get(self, request, *args, **kwargs):
        print('Token:', kwargs.get('token'))
        print('PK:', kwargs.get('pk'))

        user = get_user_model().objects.get(id=kwargs.get('pk'))
        if tokens.token_generator.check_token(user, kwargs.get('token')):
            user.is_active = True
            user.save()
            return redirect(reverse_lazy('user:login'))
        return redirect(reverse_lazy('home:landing_page'))


class ResetPasswordGenerateTokenView(FormView):
    template_name = 'user/password_reset.html'
    form_class = forms.PasswordResetEmailCheckerForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        user = get_user_model().objects.get(email=form.cleaned_data['email'])
        token = tokens.password_reset_token.make_token(user)

        models.UserResetToken.objects.create(
            user=user,
            token=token
        )

        user.email_user(
            'Reset your password',
            f'Please click on the link for a password reset:'
            f' http://{self.request.get_host()}/user/reset/{token}')

        return super().form_valid(form)


class ResetPasswordValidateTokenChangePassword(FormView):
    template_name = 'user/reset_change_password.html'
    form_class = forms.PaswordResetSetPasswordForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        user = models.UserResetToken.objects.get(token=self.kwargs.get('token')).user
        user.set_password(form.cleaned_data['new_password'])
        user.save()

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        user_token = kwargs.get('token')

        save_token = models.UserResetToken.objects.filter(token=user_token).first()

        if not save_token:
            # TODO: template with error message (token not found)
            return redirect(reverse_lazy('home:landing_page'))

        if save_token.used:
            # TODO: template with error massage (token already used)
            return redirect(reverse_lazy('home:landing_page'))

        save_token.used = True
        save_token.save()

        return super().get(request, *args, **kwargs)
