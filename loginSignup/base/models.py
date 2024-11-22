from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        extra_fields.setdefault('status', 'Active')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
    

# Create your models here.
class CustomUser(AbstractUser):

    ROLE_CHOICES = [
        ('Customer', 'Customer'),
        ('Retailer', 'Retailer'),
        ('Partner', 'Partner'),
        ('Admin', 'Admin'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')


    #we want to login with email instead of username so we are making changes ot the user model that is provided by django by default
    username = None
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(_('Email Address'), max_length=255, unique=True)
    role = models.CharField(_('Role'), max_length=10, choices=ROLE_CHOICES, null=False)
    password_hash = models.CharField(_('Password Hash'), max_length=255, null=False)
    status = models.CharField(_('Status'), max_length=10, choices=STATUS_CHOICES, default='Active')
    email_verified = models.BooleanField(_('Email Verified'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    objects = CustomUserManager()

#-----------------------------------
    def deactivate(self):
        self.status = 'Inactive'
        self.save()
#-----------------------------------


    def __str__(self):
        return f"{self.email} ({self.role})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) #save the new user model with new changes by super().save() method


# User Profile model
class UserProfile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # This ensures the foreign key uses the custom user model
        on_delete=models.CASCADE,
        related_name="profile"
    )
    first_name = models.CharField(_('First Name'), max_length=100, null=False)
    last_name = models.CharField(_('Last Name'), max_length=100, null=False)
    contact_number = models.CharField(_('Contact Number'), max_length=20, blank=True, null=True)
    preferences = models.JSONField(_('Preferences'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"