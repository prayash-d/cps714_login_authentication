from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from django.contrib import messages

from .forms import UserRegisterForm
from .models import CustomUser
from .tokens import account_activation_token

User = get_user_model()
# The User model is imported from the get_user_model() function to ensure that the user model is referenced correctly.

@login_required
def home(request):
    # Renders the home page. Requires the user to be logged in.

    user = request.user  # Get the currently logged-in user
    user_profile = user.profile  # Access the related UserProfile using related_name='profile'

    context = {
        'user': user,
        'profile': user_profile,  # Add user profile information to the context
    }

    return render(request, "home.html", context)

def login_view(request):
    if request.method == "POST":
        # Get email and password from the form
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Log in the user
            login(request, user)
            messages.success(request, "You have successfully logged out.")
            return redirect('base:home')  # Redirect to the home page or another page
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, 'registration/login.html')  # Render the login template

def logout_view(request):
    # Logs out the user and redirects to the login page
    logout(request)
    return redirect('base:login_view')

def signup_view(request):
    if request.method == "POST":
        next = request.GET.get('next')
        form = UserRegisterForm(request.POST)  # Uses UserRegisterForm from forms.py
        if form.is_valid():
            print("Signup Form is valid")
            user = form.save(commit=True)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            print(user)
            # LOG IN THE NEW USER
            new_user = authenticate(email=user.email, password=password)
            if new_user is not None:
                login(request, new_user)
            # REDIRECT TO VERIFY EMAIL
            print("Redirecting to verify_email...")
            return redirect('base:verify_email')
    else:
        form = UserRegisterForm()  # Uses UserRegisterForm from forms.py
    context = {
        'form': form
    }
    return render(request, 'registration/signup.html', context)


# 1. Verify email: send the verification link to the user’s email.
# In the code below, if the user’s email is unverified, an account activation token is generated using the account_activation_token class 
# This token can be used to verify a user through email. 
# A uid was also generated and encoded to ensure that the appropriate user _ to whom the email was sent _ gets verified.
def verify_email(request):
    # Handles email verification process
    if request.method == "POST":
        user = request.user
        current_site = get_current_site(request)
        subject = 'Activate Your Account'
        message = render_to_string('user/verify_email_message.html', {  # Uses template account_activation_email.html
            'user': user,
            'domain': current_site.domain,
            'protocol': request.scheme,
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),  # Uses account_activation_token from tokens.py
        })
        email = EmailMessage(subject, message, to=[user.email])
        email.content_subtype = 'html'
        email.send()
        print("Email sent")
        return redirect('base:verify_email_done')
    return render(request, 'user/verify_email.html')

# 2. Verify email done: tell the user to check his/her email.
def verify_email_done(request):
    # Renders the email verification done page
    return render(request, 'user/verify_email_done.html')

# 3. Verify email confirm: verify the link.
def verify_email_confirm(request, uidb64, token):
    # Verifies the email confirmation link
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):  # Uses account_activation_token from tokens.py
        user.email_verified = True
        user.save()
        return redirect('base:verify_email_complete')
    else:
        return render(request, 'user/verify_email_confirm.html')

# 4. Verify email complete: redirect the user to your website after verification.
def verify_email_complete(request):
    # Renders the email verification complete page
    return render(request, 'user/verify_email_complete.html')

def user_list(request):
    # Renders a list of all users
    users = CustomUser.objects.all()  # Uses CustomUser model from models.py
    return render(request, 'user/user_list.html', {'users': users})

# View to display the user profile for a specific user
def user_profile_view(request, user_id):
   # Fetch all users with their related profiles
    users = CustomUser.objects.select_related('profile').all()
 
    return render(request, 'user_profile.html', {'users': users})
