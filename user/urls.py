from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login', views.LoginUserView.as_view(), name='login'),
    path('register', views.RegiserUserView.as_view(), name='register'),
]