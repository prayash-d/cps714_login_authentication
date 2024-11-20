from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model, logout, update_session_auth_hash
from django.urls import reverse
from .forms import UserRegisterForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
#for user profile view
from django.shortcuts import render, get_object_or_404
from .models import CustomUser
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


User = get_user_model()
# The User model is imported from the get_user_model() function in the forms.py file.
# This is done to ensure that the user model is referenced correctly.
# so we can reference the user model as User instead of CustomUser

@login_required
def home(request):
    return render(request, "home.html", {})


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
            messages.success(request, "You have successfully logged in.")
            return redirect('base:home')  # Redirect to the home page or another page
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, 'registration/login.html')  # Render the login template

def logout_view(request):
    logout(request) #logout the user
    return redirect('base:login_view')

##this view is for the signup page
# def authView(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         email = request.POST.get('email')  # Manually extract the email
#         if form.is_valid():
#             user = form.save(commit=False)
#             password = form.cleaned_data.get('password')
#             user.set_password(password)
#             user.email = email  # Save email to user instance
#             user.save() #savigng user wuth email and password to the database

#             new_user = authenticate(email=user.email, password=password)
#             login(request, new_user)
#             if next:
#                 return redirect(next)
#             else:
#                 return redirect('verify_email') #The user is then redirected to the verify_email URL if there isn't a next parameter in the URL.

#     else:
#         form = UserCreationForm()

#     return render(request, "registration/signup.html", {"form": form})

def signup_view(request):
    if request.method == "POST":
        next = request.GET.get('next')
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print("Signup Form is valid")
            user = form.save(commit=True)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            print(user)
            #LOG IN THE NEW USER
            new_user = authenticate(email=user.email, password=password)
            login(request, new_user)
            #REDIRECT TO VERIFY EMAIL
            print("Redirecting to verify_email...")
            return redirect('base:verify_email')
    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'registration/signup.html', context)



###Views for singup email verification:
# 1. Verify email: send the verification link to the user’s email.
# 2. Verify email done: tell the user to check his/her email.
# 3. Verify email confirm: verify the link.
# 4. Verify email complete: redirect the user to your website after verification.




## send email with verification link:
# In the code below, if the user’s email is unverified, an account activation token is generated using the account_activation_token class 
# This token can be used to verify a user through email. 
# A uid was also generated and encoded to ensure that the appropriate user _ to whom the email was sent _ gets verified.
def verify_email(request):
    if request.method == "POST":
        print("verify email entered")
        if request.user.email_verified != True:
            current_site = get_current_site(request)
            user = request.user
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)

            # Debugging: Print values to console
            print("User email:", user.email)
            print("UID64:", uidb64)
            print("Token:", token)

            subject = "Verify Email"
            message = render_to_string('user/verify_email_message.html', {
                'user': user,
                'domain': current_site.domain,
                'protocol': request.scheme,
                'uidb64': uidb64,
                'token': token,
            })
            email = EmailMessage(
                subject, message, to=[user.email]
            )
            email.content_subtype = 'html'
            email.send()
            print("Email sent")
            return redirect('base:verify_email_done')
        else:
            return redirect('signup')
    return render(request, 'user/verify_email.html')


def verify_email_done(request):
    return render(request, 'user/verify_email_done.html')

#verify the link that the user clicks on...
# This view decodes the link that the user clicked on and confirms if it is valid or not. 
# If the token is valid, the email_verified field of the user is set to True and the user is redirected to the verify_email_complete URL.
# if the link is invalid, the user is sent to the verify_email_confirm.html page.

def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_verified = True
        user.save()
        messages.success(request, 'Your email has been verified.')
        return redirect('base:verify_email_complete')
    else:
        messages.warning(request, 'The verification link is invalid or has expired..')
    return render(request, 'user/verify_email_confirm.html')


def verify_email_complete(request):
    redirect_url = reverse('base:home')
    return render(request, 'user/verify_email_complete.html')

#only Admins can view this page
@login_required
def user_list(request):
    if request.user.role == 'Admin':
        users = CustomUser.objects.all()
        return render(request, 'user/user_list.html', {'users': users})
    else:
        return HttpResponse("You are not authorized to view this page.")

# View to display the user profile for a specific user
def user_profile_view(request, user_id):
   # Fetch all users with their related profiles
    users = CustomUser.objects.select_related('profile').all()
 
    return render(request, 'user_profile.html', {'users': users})


