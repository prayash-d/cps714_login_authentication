from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile, CustomUser

User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        label_suffix= '',
        widget=forms.PasswordInput(attrs={'placeholder': ''}),
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        label_suffix= '',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
    )

    role = forms.ChoiceField(
        label='Role',
        label_suffix= '',
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={'placeholder': 'Select your role', 'class': 'form-dropdown'}),
    )
    # Fields from the UserProfile model
    first_name = forms.CharField(
        label='First Name',
        label_suffix= '',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'John'}),
    )
    last_name = forms.CharField(
        label='Last Name',
        label_suffix= '',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Smith'}),
    )
    contact_number = forms.CharField(
        label='Phone Number',
        label_suffix= '',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. 1235467890'}),
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'role']  # Fields from the CustomUser model
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match. Please try again.")

        if password and len(password) < 5:
            self.add_error('password', "Password must be at least 5 characters long.")

        return cleaned_data

    def save(self, commit=True):
        # Save the user first
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
            print(f"User {user.email} saved successfully")  # Debugging statement

          # Now save the profile fields
        UserProfile.objects.create(
            user=user,  # Associate the user after it's saved
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            contact_number=self.cleaned_data.get('contact_number', '')
        )
        print(f"UserProfile for {user.email} created successfully")  # Debugging statement
        return user