from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile, CustomUser

User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email Address',
        label_suffix= '*',
        widget=forms.EmailInput(attrs={'placeholder': 'joannesmith@greengrove.com'}),
    )
    password = forms.CharField(
        label='Password',
        label_suffix= '*',
        widget=forms.PasswordInput(attrs={'placeholder': ''}),
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        label_suffix= '*',
        widget=forms.PasswordInput(attrs={'placeholder': ''}),
    )

    role = forms.ChoiceField(
        label='Role',
        label_suffix= '*',
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={'placeholder': 'Select your role', 'class': 'form-dropdown'}),
    )
    # Fields from the UserProfile model
    first_name = forms.CharField(
        label='First Name',
        label_suffix= '*',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Joanne'}),
    )
    last_name = forms.CharField(
        label='Last Name',
        label_suffix= '*',
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
    # Meta class to specify the model and fields to be used
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'role']  # Fields from the CustomUser model
    
    # form field order
    field_order = ['first_name', 'last_name', 'email', 'contact_number', 'password', 'confirm_password', 'role']

     # Clean the form data add check for errors   
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Check if password and confirm_password match
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match. Please try again.")

        # Check if password is at least 8 characters long
        if password and len(password) < 8:
            self.add_error('password', "Password must be at least 8 characters long.")

            # Check if the password contains at least 3 numbers
        if password:
            digit_count = sum(char.isdigit() for char in password)
            if digit_count < 3:
                self.add_error('password', "Password must contain at least 3 numbers.")

        return cleaned_data

    # Save the user and profile data when the form is submitted
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