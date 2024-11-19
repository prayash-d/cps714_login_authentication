from django.urls import path, include
from .views import home, signup_view, verify_email, verify_email_done, verify_email_confirm, verify_email_complete, user_list
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('login/', views.login_view, name='login_view'),
    path("signup/", views.signup_view, name="signup_view"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('verify_email/done/', views.verify_email_done, name='verify_email_done'),
    path('verify_email_confirm/<uidb64>/<token>/', views.verify_email_confirm, name='verify_email_confirm'),
    path('verify_email/complete/', views.verify_email_complete, name='verify_email_complete'),

    path('all_users/', views.user_list, name='user_list'),
]