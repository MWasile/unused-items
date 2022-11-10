from django.views.generic import TemplateView, FormView, View
from django.contrib.auth import login, logout, get_user_model
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

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

    def get_context_data(self, **kwargs):
        info = self.kwargs['info']
        context = super().get_context_data(**kwargs)
        print(info, 'XDDD')
        if info == 'donations_in_progress' or not info:
            context['donations_in_progress'] = Donation.objects.filter(user=self.request.user, is_taken=False)
        elif info == 'realized_donations':
            context['realized_donations'] = Donation.objects.filter(user=self.request.user, is_taken=True)
        elif info == 'user_detail':
            context['user_detail'] = get_user_model().objects.get(pk=self.request.user.pk)

        print(context)

        return context


class UserDonationUpdateStatusView(View):
    def get(self, request, *args, **kwargs):
        donation = Donation.objects.get(id=kwargs.get('pk'))
        donation.is_taken = True
        donation.save()
        return redirect(reverse_lazy('user:detail', kwargs={'info': 'donations_in_progress'}))


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
        user = get_user_model().objects.get(id=kwargs.get('pk'))

        if tokens.token_generator.check_token(user, kwargs.get('token')):
            user.is_active = True
            user.save()
            messages.success(request, 'Dzękujemy za aktywację konta!')
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

        messages.success(self.request, 'Email z linkiem do zmiany hasła został wysłany!')

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

        messages.success(self.request, 'Hasło zostało zmienione!')
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        user_token = kwargs.get('token')

        save_token = models.UserResetToken.objects.filter(token=user_token).first()

        if not save_token:
            messages.error(request, 'Link do zmiany hasła jest nieprawidłowy!')
            return redirect(reverse_lazy('user:login'))

        if save_token.used:
            messages.error(request, 'Link do zmiany hasła został już wykorzystany!')
            return redirect(reverse_lazy('user:login'))

        save_token.used = True
        save_token.save()

        return super().get(request, *args, **kwargs)
