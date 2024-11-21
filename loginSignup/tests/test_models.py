from django.test import TestCase
from base.models import CustomUser, UserProfile

# To run this specific file use the command: python manage.py test tests.test_models
#All tests sucessful
class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='securepassword',
            role='Customer'
        )

    def test_create_user(self):
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('securepassword'))
        self.assertEqual(self.user.role, 'Customer')

    def test_user_profile_creation(self):
        profile = UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            contact_number='1234567890'
        )
        self.assertEqual(profile.first_name, 'Test')
        self.assertEqual(profile.last_name, 'User')
        self.assertEqual(profile.contact_number, '1234567890')
