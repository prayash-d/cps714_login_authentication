from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from base.tokens import account_activation_token
from base.models import CustomUser, UserProfile

User = get_user_model()

# To run this specific file use the command: python manage.py test tests.test_views
class ViewTests(TestCase):

    def setUp(self):
        # Create a user and a user profile for testing
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='securepassword',
            role='Customer',
            email_verified=False
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            contact_number='1234567890'
        )

    def test_home_view_authenticated(self):
        self.client.login(email='testuser@example.com', password='securepassword')
        response = self.client.get(reverse('base:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'John')  # Ensuring profile data is included

    def test_home_view_not_authenticated(self):
        response = self.client.get(reverse('base:home'))
        self.assertEqual(response.status_code, 302)  # Redirects to login page


    def test_login_view_invalid_credentials(self):
        response = self.client.post(reverse('base:login_view'), {
            'email': 'wronguser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid email or password.')

    def test_logout_view(self):
        self.client.login(email='testuser@example.com', password='securepassword')
        response = self.client.get(reverse('base:logout_view'))
        self.assertEqual(response.status_code, 302)  # Redirects to login page
        self.assertRedirects(response, reverse('base:login_view'))

    def test_signup_view_valid_data(self):
        response = self.client.post(reverse('base:signup_view'), {
            'email': 'newuser@example.com',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123',
            'role': 'Customer',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'contact_number': '0987654321'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_signup_view_invalid_data(self):
        response = self.client.post(reverse('base:signup_view'), {
            'email': 'invalid-email',
            'password': 'securepassword',
            'confirm_password': 'mismatchpassword',
            'role': 'Customer',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Passwords do not match')

    def test_verify_email_view(self):
        self.client.login(email='testuser@example.com', password='securepassword')
        response = self.client.post(reverse('base:verify_email'))
        self.assertEqual(response.status_code, 302)  # Redirects to verify_email_done
        self.assertRedirects(response, reverse('base:verify_email_done'))
        self.assertEqual(len(mail.outbox), 1)  # Email should be sent

    def test_verify_email_confirm_view_valid(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)
        response = self.client.get(reverse('base:verify_email_confirm', kwargs={'uidb64': uidb64, 'token': token}))
        self.assertEqual(response.status_code, 302)  # Redirects to verify_email_complete
        self.assertTrue(User.objects.get(email='testuser@example.com').email_verified)

    def test_verify_email_confirm_view_invalid(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = 'invalid-token'
        response = self.client.get(reverse('base:verify_email_confirm', kwargs={'uidb64': uidb64, 'token': token}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/verify_email_confirm.html')

    def test_user_list_view(self):
        # Admin user required to access this view
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword',
            role='Admin'
        )
        self.client.login(email='admin@example.com', password='adminpassword')
        response = self.client.get(reverse('base:user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser@example.com')

    # def test_user_profile_view(self):
    #     response = self.client.get(reverse('base:user_profile_view', kwargs={'user_id': self.user.pk}))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'John Doe')

def setUp(self):
        self.admin_user = CustomUser.objects.create_user(
            email="admin@example.com", password="adminpass", role="Admin", status="Active"
        )
        self.regular_user = CustomUser.objects.create_user(
            email="user@example.com", password="userpass", role="Customer", status="Active"
        )

def test_activate_user(self):
    self.client.login(email="admin@example.com", password="adminpass")
    response = self.client.post(reverse('base:user_list'), {
        'user_id': self.regular_user.user_id,
        'action': 'deactivate'
    })
    self.regular_user.refresh_from_db()
    self.assertEqual(self.regular_user.status, 'Inactive')

def test_login_inactive_user(self):
    self.regular_user.status = "Inactive"
    self.regular_user.save()
    response = self.client.post(reverse('base:login_view'), {
        'email': 'user@example.com',
        'password': 'userpass'
    })
    self.assertContains(response, "Your account has been deactivated, please contact support for assistance.")