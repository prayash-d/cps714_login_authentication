from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
    )

    class Meta:
        model = User
        fields = ['email', 'password']

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError("This email is already registered. Please use a different one.")
    #     return email

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
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user
