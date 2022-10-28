from django.db.models.aggregates import Sum
from django.views.generic import TemplateView

from . import models


class LandingPageView(TemplateView):
    template_name = 'home/landingpage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['counts'] = {
            'institutions_count': models.Institution.objects.count(),
            'bags_count': models.Donation.objects.aggregate(Sum('quantity'))
        }
        context['org'] = {
            'FUN': models.Institution.objects.filter(type='FUN')[:3],
            'NGO': models.Institution.objects.filter(type='NGO')[:3],
            'LOC': models.Institution.objects.filter(type='LOC')[:3]
        }
        return context


class AddDonationView(TemplateView):
    template_name = 'home/form.html'
