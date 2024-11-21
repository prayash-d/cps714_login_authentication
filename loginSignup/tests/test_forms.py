from django.test import TestCase
from base.forms import UserRegisterForm

#TO run this specific file use the command: python manage.py test tests.test_forms 
#all tests successful
class UserRegisterFormTests(TestCase):
    
    def test_valid_form(self):
        form_data = {
            'email': 'validuser@example.com',
            'password': 'securepassword',
            'confirm_password': 'securepassword',
            'role': 'Customer',
            'first_name': 'John',
            'last_name': 'Doe',
            'contact_number': '1234567890',
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        form_data = {
            'email': 'validuser@example.com',
            'password': 'password123',
            'confirm_password': 'password456',
            'role': 'Customer',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('confirm_password', form.errors)
    
    def test_invalid_email(self):
        form_data = {
            'email': 'notanemail',
            'password': 'securepassword',
            'confirm_password': 'securepassword',
            'role': 'Customer',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_password_too_short(self):
        form_data = {
            'email': 'validuser@example.com',
            'password': '123',
            'confirm_password': '123',
            'role': 'Customer',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_missing_first_name(self):
        form_data = {
            'email': 'validuser@example.com',
            'password': 'securepassword',
            'confirm_password': 'securepassword',
            'role': 'Customer',
            'last_name': 'Doe',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_missing_last_name(self):
        form_data = {
            'email': 'validuser@example.com',
            'password': 'securepassword',
            'confirm_password': 'securepassword',
            'role': 'Customer',
            'first_name': 'John',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)
