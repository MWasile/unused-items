from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing_page'),
    path('<str:fundation_type>', views.LandingPageView.as_view(), name='landing_page_args'),
    path('donation/', views.AddDonationView.as_view(), name='add_donation'),
    path('donation/confirmation/', views.DonationConfirmationView.as_view(), name='donation_confirmation'),
    path('send/contact-form', views.ContactFormView.as_view(), name='contact_form')
]
