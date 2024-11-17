from django.urls import path, include
from .views import home, signup_view, verify_email, verify_email_done, verify_email_confirm, verify_email_complete
from . import views

urlpatterns = [
    path("", home, name="home"),
    path('login/', views.login_view, name='login'),
    path("signup/", views.signup_view, name="signup_view"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('verify_email/done/', views.verify_email_done, name='verify_email_done'),
    path('verify_email_confirm/<uidb64>/<token>/', views.verify_email_confirm, name='verify_email_confirm'),
    path('verify_email/complete/', views.verify_email_complete, name='verify_email_complete'),
]