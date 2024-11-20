from django.contrib import admin
from django.urls import path, include, reverse_lazy
from base import views
from django.contrib.auth import views as auth_views

app_name = 'base'

urlpatterns = [
     path("home/", views.home, name="home"),
     path("", views.login_view, name="login"),
     path('login/', views.login_view, name='login_view'),
     path('logout/', views.logout_view, name='logout_view'),
     path("signup/", views.signup_view, name="signup_view"),
     # path("accounts/", include("django.contrib.auth.urls")),
     path('verify_email/', views.verify_email, name='verify_email'),
     path('verify_email/done/', views.verify_email_done, name='verify_email_done'),
     path('verify_email_confirm/<uidb64>/<token>/', views.verify_email_confirm, name='verify_email_confirm'),
     path('verify_email/complete/', views.verify_email_complete, name='verify_email_complete'),

     path('all_users/', views.user_list, name='user_list'),

     path('password-reset/', auth_views.PasswordResetView.as_view(template_name= 'registration/password_reset_form.html',
                                                                  email_template_name = 'registration/password_reset_email.html',
                                                                  success_url= reverse_lazy('base:password_reset_done')),
                                                                  name='password_reset'),
     path('password-reset-confirm/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html', success_url= reverse_lazy('base:password_reset_complete')),
          name='password_reset_confirm'),
     path('password-reset-complete/',
          auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
          name='password_reset_complete'),
     path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
                                                                 template_name='registration/password_reset_done.html'),
                                                                 name='password_reset_done'),

     #     path('password-reset/', views.request_password_reset, name='password_reset'),
     #     path('password-reset-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
     #     path('password-reset-complete/', views.password_reset_complete, name='password_reset_complete'),


  
]
# This adds the following password reset endpoints:

# /password-reset/: Request password reset via email.
# /password-reset/done/: Confirmation after submitting the email.
# /reset/<uidb64>/<token>/: Link for the user to reset their password.
# /reset/done/: Confirmation after successfully resetting the password.