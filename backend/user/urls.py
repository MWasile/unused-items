from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login', views.LoginUserView.as_view(), name='login'),
    path('register', views.RegiserUserView.as_view(), name='register'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path('detail/<str:info>', views.UserDetailView.as_view(), name='detail'),
    path('donation/<int:pk>', views.UserDonationUpdateStatusView.as_view(), name='taken'),
    path('password', views.UserChangePasswordView.as_view(), name='password'),
    path('activate/<int:pk>/<str:token>', views.ActivateUserView.as_view(), name='activate'),
    path('reset_password', views.ResetPasswordGenerateTokenView.as_view(), name='reset_password'),
    path('reset/<str:token>', views.ResetPasswordValidateTokenChangePassword.as_view(),
         name='reset_password_token'),
]
