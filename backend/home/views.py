import json

from django.http import HttpResponse
from django.db import DatabaseError
from django.db.models.aggregates import Sum
from django.views.generic import TemplateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect

from . import models


class LandingPageView(ListView):
    template_name = 'home/landingpage.html'
    model = models.Institution
    context_object_name = 'institutions'
    paginate_by = 5
    ordering = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['counts'] = {
            'institutions_count': self.model.objects.count(),
            'bags_count': models.Donation.objects.aggregate(Sum('quantity'))
        }
        return context

    def get_queryset(self):
        if not self.kwargs.get('fundation_type'):
            return models.Institution.objects.filter(type='FUN')
        return models.Institution.objects.filter(type=self.kwargs['fundation_type'].strip())


class AddDonationView(LoginRequiredMixin, TemplateView):
    template_name = 'home/form.html'
    login_url = reverse_lazy('user:login')
    redirect_field_name = reverse_lazy('user:register')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = models.Category.objects.all()
        context['institutions'] = models.Institution.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data_from_user = json.loads(self.request.body)
        try:
            donation = models.Donation.objects.create(
                quantity=data_from_user['bagCount'],
                institution_id=data_from_user['organizationId'],
                address=data_from_user['userStreet'],
                phone_number=data_from_user['userPhone'],
                city=data_from_user['userCity'],
                zip_code=data_from_user['userPostCode'],
                pick_up_date=data_from_user['userDate'],
                pick_up_time=data_from_user['userTime'],
                pick_up_comment=data_from_user['userPickUpComment'],
                user=self.request.user,
                # TODO: Set default value in model
            )
            donation.save()
            return HttpResponse(status=200)

        except DatabaseError:
            return HttpResponse(status=400)


class DonationConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = 'home/form-confirmation.html'


class ContactFormView(View):
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body)

        name, email, message = data['userName']['value'], data['userEmail']['value'], data['userMessage']['value']

        if not name or not email or not message:
            return HttpResponse(status=400)

        try:
            user_message = models.UserMessageToAdmin.objects.create(
                name=name,
                email=email,
                message=message
            )
            user_message.save()
            return HttpResponse(status=200, content='Wiadomość została wysłana')
        except DatabaseError:
            return HttpResponse(status=400, content='Wystąpił błąd podczas wysyłania wiadomości')
