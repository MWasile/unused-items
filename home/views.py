from django.views.generic import TemplateView


class LandingPageView(TemplateView):
    template_name = 'home/landingpage.html'


class AddDonationView(TemplateView):
    template_name = 'home/form.html'
