from django.views.generic import TemplateView, FormView
from django.contrib.auth import login
from django.urls import reverse_lazy

from . import forms


class LoginUserView(TemplateView):
    template_name = 'user/login.html'


class RegiserUserView(FormView):
    template_name = 'user/register.html'
    form_class = forms.ReigsterUserForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        new_user = form.create_new_user()
        return super().form_valid(form)
