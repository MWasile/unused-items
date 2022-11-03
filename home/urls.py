from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing_page'),
    path('<str:fundation_type>', views.LandingPageView.as_view(), name='landing_page_args'),
    path('donation/', views.AddDonationView.as_view(), name='add_donation'),
]
