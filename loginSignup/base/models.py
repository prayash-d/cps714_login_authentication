from django.db import models
###DO this when you make changes to this file:
# 1. Change your models (in models.py).

# 2. Run python manage.py makemigrations to create migrations for those changes

# 3.  Run python manage.py migrate to apply those changes to the database.


# # Create your models here.
from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Retailer', 'Retailer'),
        ('Customer', 'Customer'),
        ('Partner', 'Partner'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True, null=False)
    password_hash = models.CharField(max_length=255, null=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_id} - {self.email} - {self.role}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    preferences = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Profile"