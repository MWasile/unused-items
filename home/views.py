from django.db.models.aggregates import Sum
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

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
        return context
